# This file is part of SOCAD
# Copyright (C) 2018  Miguel Fernandes
#
# SOCAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SOCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""Main module."""

import sys

from util import print_menu
from socad import Client


def load_simulator(client):
    """Load the Cadence simulator.

    This task is performed once per run (contrary to the Cadence ADE) that
    loads the simulator everytime we run a simulation, which is very
    inefficient.

    Arguments:
        client {handler} -- client that communicates with the simulator

    Raises:
        TypeError -- if the server response is not from the expected type

    Returns:
        dict -- circuit design variables
    """
    req = dict(type='loadSimulator', data=None)
    client.send_data(req)
    res = client.recv_data()

    try:
        res_type = res['type']
        data = res['data']
    except KeyError as err:  # if the key does not exist
        raise KeyError(err)

    if res_type != 'loadSimulator':
        raise TypeError('The response type should be "loadSimulator"!!!')

    return data


def process_server_response(res):
    """Process a response received from the server.
    
    Args:
        res (dict): server response
    
    Raises:
        KeyError: if the received data is corrupted
        KeyError: if the received data is invalid
    
    Returns:
        tuple: type of response, received data
    """
    try:
        typ = res['type']
        data = res['data']
    except KeyError as err:  # if the key does not exist
        raise KeyError(err)

    # If response type is loadSimulator we want to receive the original (user defined)
    # circuit variables.
    if 'loadSimulator' in typ:
        print("\nSimulator loaded with success! Received variables:")
        for key, val in data.items():
            print(f"Variable: {key} - Value: {val}")

        return 'vars', data
    # If response type is updateAndRun we want to receive simulation results to
    # fed into the optimizer
    elif 'updateAndRun' in typ:
        print('\nReceived updateAndRun from Cadence')

        print(f"Simulation results: {data}")

        return 'results', data
    else:
        raise KeyError("Invalid data received from server.")


def main():
    """Main function"""

    # Print license
    print("\nSOCAD  Copyright (C) 2018  Miguel Fernandes")
    print("This program comes with ABSOLUTELY NO WARRANTY.")
    print("This is free software, and you are welcome to redistribute it under the terms")
    print("of the GNU General Public License as published by the Free Software Foundation,")
    print("either version 3 of the License, or (at your option) any later version.")
    print("For more information, see <http://www.gnu.org/licenses/>\n")

    try:
        print("Starting client...")
        client = Client()
    except OSError as err:
        print(f"[SOCKET ERROR] {err}")
        print("\n**** Ending program... Bye! ****")
        return 1

    host = "localhost"
    port = 3000

    try:
        print("Connecting to server...")
        addr = client.run(host, port)
        print(f"[INFO] Connected to server with the address {addr[0]}:{addr[1]}")

        data = {}
        variables = {}  # Circuit variables (to be optimized)

        # Main loop
        while True:
            option = print_menu()

            if option == 1:
                req = dict(type='loadSimulator', data='ola')
            elif option == 2:
                print("\nSending updated variables...")
                for key, val in variables.items():
                    print(f"Key: {key} - Val:{val}")
                req = dict(type='updateAndRun', data=variables)
            else:
                if option:  # if option != 0
                    print("Wrong option!!!")
                print("Shutting down.")
                req = dict(type='info', data='exit')
                client.send_data(req)
                break

            # Send data to server
            client.send_data(req)

            # Wait for data from server
            res = client.recv_data()

            typ, data = process_server_response(res)

            if typ == 'vars':
                variables = data
            elif typ == 'results':
                # results = data
                for key, val in variables.items():
                    variables[key] = val * 1.1
            else:
                raise KeyError(f"Invalid data type: {typ}")

        # End the program
        req = dict(type='info', data='exit')
        client.send_data(req)

    except ConnectionError as err:
        print(f"[CONNECTION ERROR] {err}")
        return 2
    except (TypeError, ValueError) as err:
        print(f"[TYPE/VALUE ERROR] {err}")
        return 3
    except KeyError as err:
        print(f"[KEY ERROR] {err}")
        return 4
    finally:
        print("\n**** Closing socket and ending program... Bye! ****")
        client.close()  # Close the client socket

    return 0


if __name__ == "__main__":
    sys.exit(main())
