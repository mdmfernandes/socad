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
"""Server that stands between a client and Cadence Virtuoso."""

import json
import socket
import struct
import time
from contextlib import contextmanager


@contextmanager
def closing(thing):
    """Close stream when using the "with" since the __close__ method of
    streams is not defined in python 2.

    Arguments:
        thing (stream): stream (file, socket, ...)
    """
    try:
        yield thing
    finally:
        thing.close()


class Server:
    """A server that handles skill commands.

    This server is started and ran by Cadence Virtuoso. It receives data from
    a client and passes it to Cadence. It then gather the Cadence response and
    send it back to the client. The data sent to client is serialized in JSON
    and the data from client should also be in JSON.

    Arguments:
        cad_stream (object): Cadence stream.
        sock (object, optional): socket to use in the connection
            (default: None).        
    """

    def __init__(self, cad_stream, sock=None):
        """Create the server socket."""
        self.cad_stream = cad_stream
        self.server_in = cad_stream.stdin
        self.server_out = cad_stream.stdout
        self.server_err = cad_stream.stderr

        # Uninitialized variables
        self.conn = None  # Client socket

        # Receive initial message from cadence, to check connectivity, and send it back
        # to print on screen
        msg = self.recv_skill()
        self.send_skill(msg)

        if sock is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # define socket options to allow the reuse of the same addr
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.socket = sock

    def run(self, host, port):
        """Start the server.

        Arguments:
            host (str): remote socket IP address.
            port (int): remote socket port.

        Raises:
            ConnectionError: if there's a communication problem.

        Returns:
            list: remote socket name.
        """
        try:
            # Start connection between client and server (UNIX socket)
            # NOTE: After the connection with the client, the "self.conn" is the socket
            # that communicates with the client, so the "self.socket" is not required
            # anymore and can be closed.
            with closing(self.socket) as s:
                s.bind((host, port))
                s.listen(1)  # Waits for client connection

                # Accept the client connection and get his socket and address
                self.conn, addr = s.accept()
        except OSError as err:
            raise IOError(err)  # TODO: Replace to "ConnectionError"

        # The next function calls don't need a try statement because if they
        # have an exception the error will be caught in the function that
        # calls this one

        # Send the socket address to the client
        self.send_data(dict(data=addr))

        # Receive remote socket name
        return self.recv_data()['data']

    def send_data(self, obj):
        """Send an object through a socket.

        1 - Serialize the object in JSON and encode the string;

        2 - pack the serialized object length in an unsigned int (I) [4 bytes],
            and big-endian byte order (>) (this way the *object size* message
            has always the same size);

        3 - send the data.

        Arguments:
            obj (dict): object to send.

        Raises:
            TypeError: if the object is not serializable in JSON.
            ConnectionError: if the socket connection is broken.
        """
        # Serialize the object in JSON and encode the string as a bytes object
        try:
            serialized = json.dumps(obj).encode()
        except (TypeError, ValueError):
            raise TypeError('It can only send JSON-serializable data')

        serialized_len = len(serialized)  # String length

        # Packed string length
        pack_serialized_len = struct.pack('>I', serialized_len)

        # Data to send
        data = pack_serialized_len + serialized

        total_sent = 0

        while total_sent < serialized_len:
            sent = self.conn.send(data[total_sent:])

            if not sent:
                # TODO: Replace to "ConnectionError"
                raise IOError("Socket connection broken while sending data")

            total_sent += sent

    def recv_data(self):
        """Receive an object through a socket.

        1 - Receive the first 4 bytes of data, which contains the data length;

        2 - Receive the data, serialized in JSON, and decode it;

        3 - Convert the received data in an object.

        Raises:
            ConnectionError: if the socket connection is broken.
            TypeError: if the received data is not in JSON format.

        Returns:
            dict: decoded and de-serialized received data.
        """
        data_len = self.recv_bytes(4)

        if not data_len:
            # TODO: Replace to "ConnectionError"
            raise IOError("Socket connection broken while receiving data")

        msg_len = struct.unpack('>I', data_len)[0]

        serialized = self.recv_bytes(msg_len).decode()

        try:
            obj = json.loads(serialized)
        except (TypeError, ValueError):
            raise TypeError('Received data is not in JSON format')

        return obj

    def recv_bytes(self, n_bytes):
        """Receive a specified number of bytes through a socket.

        Arguments:
            n_bytes (int): number of bytes to receive.

        Raises:
            ConnectionError: if the socket connection is broken.

        Returns:
            bytes: received bytes stream.
        """
        data = b''  # Bytes literal
        data_len = len(data)

        while data_len < n_bytes:
            # Receives a maximum of 1024 bytes per iteration
            packet = self.conn.recv(min(n_bytes - data_len, 1024))

            if not packet:
                # TODO: Replace to "ConnectionError"
                raise IOError("Socket connection broken while receiving bytes")

            data_len += len(packet)
            data += packet

        return data

    def send_skill(self, expr):
        """Send a skill expression to Cadence Virtuoso for evaluation.

        Arguments:
            data (str): skill expression.
        """
        self.server_out.write(expr)
        self.server_out.flush()

    def recv_skill(self):
        """Receive a response from Cadence.

        First receives the message length (number of bytes) and then receives
        the message.

        Returns:
            str: message received from Cadence Virtuoso.
        """
        num_bytes = int(self.server_in.readline())
        msg = self.server_in.read(num_bytes)

        # Remove the '\n' from the message
        if msg[-1] == '\n':
            msg = msg[:-1]

        return msg

    def send_warn(self, warn):
        """Send a warning message to Cadence Virtuoso.

        Arguments:
            warn (str): warning message.
        """
        self.server_err.write(warn)
        self.server_err.flush()

    def send_debug(self, msg):
        """Send a debug message to Cadence Virtuoso.

        Arguments:
            msg (str): debug message.
        """
        time.sleep(1)  # Wait a second before send the message
        self.send_warn("[Debug] {0}".format(msg))

    def close(self, code):
        """Close the server socket and end the communication with Cadence.

        Arguments:
            code (int): exit code.
        """
        self.conn.close()
        # Send feedback to Cadence
        self.send_warn("Connection with the client ended!\n\n")
        self.server_out.close()  # close stdout
        self.server_err.close()  # close stderr
        self.cad_stream.exit(code)  # close connection to cadence (code up to 255)
