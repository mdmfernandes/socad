; This file is part of SOCAD
; Copyright (C) 2018 Miguel Fernandes
;
; SOCAD is free software: you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation, either version 3 of the License, or
; (at your option) any later version.
;
; SOCAD is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
; GNU General Public License for more details.

; You should have received a copy of the GNU General Public License
; along with this program. If not, see <http://www.gnu.org/licenses/>.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Simulation related functions     ;;
;;  - Load the simulator            ;;
;;  - Update design variables       ;;
;;  - Run a simulation from ADE     ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Load the simulator by running the provided file.
;; 
;; @param {string} loadFile - name of file to load the simulator from
;;
procedure( loadSimulator(loadFile)

    print("[INFO] Loading the simulator")
    ; Load the simulator
    load(loadFile)
    
    ; Send the function status to the server
    msg = "loadSimulator_OK"
)

;; Update the circuit design variables and run a simulation.
;;
;; @param {string} runFile - name of file to run the simulation from
;; @param {string} varFile - name of file with the circuit design variables
;; @param {string} resultFile - name of file to store the simulation results
;;
procedure( updateAndRun(runFile varFile resultFile)

    ; Load the circuit variables
    load(varFile)

    ; Set the results file
    setShellEnvVar(resultFile)

    ; run the simulation
    load(runFile) 

    ; Send the function status to the server
    msg = "updateAndRun_OK"
)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Server related functions         ;;
;;  - Start python server           ;;
;;  - Handle server requests        ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Send data to server. First it sends the data size and then the message
;; 
;; @param {number} cid - Server handle
;; @param {string} msg - data to send
;;
procedure( sendData(cid msg)
    printf("[INFO] Sending message to server: %s\n" msg)
    ; First sends the size of the data to send
    ipcWriteProcess(cid sprintf(nil "%d\n" strlen(msg)))
    ; Then sends the data
    ipcWriteProcess(cid msg)
)


;; Handles requests from the server (through stdout)
;; 
;; @param {number} cid - Server handle
;; @param {string} request - Request received from the server
;;
procedure( requestHandler(cid request)
	let( (result resultStr)
        if( serverHasStarted <= 0 then
            if( request == "Python server has started!" then
                serverHasStarted = 1
                printf("[INFO] Cadence is connected to server! Waiting for a connection from the client...\n")
            else
                printf("[INFO] Waiting for server... Message: %s\n" request)
            )
        else    ; if the server is running
            ; if the request is to call a function
            if( rexMatchp("(.*)" request) then
                ; The "errsetstring" evaluates the request and returns the result,
                ; if valid, or an error message. E.g. if the request is a function,
                ; it executes the function and returns the result.
                if( result = errsetstring(request 't) then
                    sprintf(resultStr "%L\n" car(result))
                else
                    sprintf(resultStr "%s\n" car(nthelem(5 errset.errset)))
                )
                sendData(cid resultStr)
            else
                printf("[INFOs] %s\n" request)
            )
        )
    )
)


;; Handles server errors (through the stderr)
;; 
;; @param {number} cid - Server handle
;; @param {string} errorMessage - Error message received from the server
;;
procedure( errorHandler(cid errorMessage)
	warn("%s\n" errorMessage)
)


;; Handles the server shutdown
;; 
;; @param {number} cid - Server handle
;; @param {number} exitStatus - Server exit status
;;
procedure( exitHandler(cid exitStatus)
	printf("Server has stopped with the exit code %d. I'm out!!!\n" exitStatus)
    hiRegTimer("exit()", 10)    ; exit Cadence
)


;; Starts the python server as child process for inter-process communication
;;
procedure( startServer()
	printf("[INFO] Starting server process...\n")
    serverHasStarted = 0
	cid = ipcBeginProcess("sh run_server.sh" "" 'requestHandler 'errorHandler 'exitHandler "")
    msg = "Python server has started!\n"
    ipcWriteProcess(cid sprintf(nil "%d\n" strlen(msg)))
	ipcWriteProcess(cid msg)
)

serverHasStarted = 0
; Starts the server
startServer()