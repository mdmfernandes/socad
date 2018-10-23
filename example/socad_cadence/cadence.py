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
"""This module handles the communication between Cadence and the server."""

import os
import sys

import util

# Try to import 'Server' from the global package 'socad'
try:
    from socad import Server
except ImportError as err:
    # If can't import from the global package
    try:  # Try to import from server.py
        from interface.server import Server
    except ImportError as err:
        # If can't import the package, quit the program
        print("[ERROR] {0}. Exiting...".format(err))
        sys.exit('1')

# Simulator files
SIM_FILE = os.environ.get('SOCAD_SCRIPT_DIR') + "/loadSimulator.ocn"
RUN_FILE = os.environ.get('SOCAD_SCRIPT_DIR') + "/run.ocn"
VAR_FILE = os.environ.get('SOCAD_SCRIPT_DIR') + '/vars.ocn'
OUT_FILE = os.environ.get('SOCAD_ROOT_DIR') + "/sim_res"


def process_skill_request(req):
    """Process a skill request from the client.

    Based on the given request object, returns the skill expression to be
    evaluated by Cadence.

    Arguments:
        req {dict} -- request object

    Raises:
        KeyError -- if the input request format is invalid
        TypeError -- if the type parameter of the received object is invalid

    Returns:
        str -- expression to be evaluated by Cadence
    """
    try:
        type_ = req['type']
        data = req['data']
    except KeyError as err:  # if the key does not exist
        raise KeyError(err)

    if type_ == 'info' and data.lower() == 'exit':
        res = 'exit'

    elif type_ == 'loadSimulator':
        res = 'loadSimulator( "{0}")'.format(SIM_FILE)

    elif type_ == 'updateAndRun':
        # Store circuit variables in file
        util.store_vars_in_file(data, VAR_FILE)
        res = 'updateAndRun("{0}" "{1}" "SOCAD_RESULT_FILE={2}")'.format(RUN_FILE, VAR_FILE, OUT_FILE)
    else:
        raise TypeError("Invalid object received from the client.")

    return res


def process_skill_response(msg):
    """Process the skill response from Cadence.

    Arguments:
        msg {str} -- cadence response

    Raises:
        TypeError -- if the input message format is invalid

    Returns:
        tuple -- response type (type_) and response object (obj)
    """
    if "loadSimulator_OK" in msg:
        type_ = 'loadSimulator'
        # Get the original circuit variables (user defined) to send
        var = util.get_vars_from_file(VAR_FILE)
        obj = var

    elif "updateAndRun_OK" in msg:
        type_ = 'updateAndRun'
        # Get the results from file
        obj = util.get_results_from_file(OUT_FILE)

    else:
        raise TypeError("Invalid message received from Cadence.")

    return type_, obj


def main():
    """Module main function."""
    try:
        # Start the server
        server = Server(sys)
    except OSError as err:
        server.send_warn("[SOCKET ERROR] {0}".format(err))
        return 1

    host = os.environ.get('SOCAD_CLIENT_ADDR')
    port = int(os.environ.get('SOCAD_CLIENT_PORT'))

    try:
        addr = server.run(host, port)

        # Log the connectivity to Cadence
        log = "Connected to client with address {0}:{1}".format(addr[0], addr[1])
        server.send_skill(log)

    except IOError as err:  # NOTE: "ConnectionError" nao existe no Python 2 -_-
        server.send_warn("[CONNECTION ERROR] {0}".format(err))
        return 2

    code = 0    # Return code
    try:
        while True:
            # Wait for a client request
            req = server.recv_data()

            # Process the client request
            expr = process_skill_request(req)

            if expr == 'exit':
                break
            else:
                # Send the request to Cadence
                server.send_skill(expr)
                # Wait for a response from Cadence
                res = server.recv_skill()
                # Process the Cadence response
                typ, obj = process_skill_response(res)
                # Send the processed response to the client
                server.send_data(dict(type=typ, data=obj))

    except IOError as err:  # NOTE: "ConnectionError" nao existe no Python 2 -_-
        server.send_warn("[CONNECTION ERROR] {0}".format(err))
        code = 3
    except TypeError as err:
        server.send_warn("[TYPE ERROR] {0}".format(err))
        code = 4
    except KeyError as err:
        server.send_warn("[KEY ERROR] {0}".format(err))
        code = 5

    server.close(code)
    return code


if __name__ == "__main__":
    sys.exit(main())
