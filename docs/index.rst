.. SOCAD documentation master file, created by
   sphinx-quickstart on Sat Oct 13 15:44:08 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SOCAD documentation
===================

SOCAD connects Cadence Virtuoso to a Python client. The communication between both processes is made through a server, using the following mechanisms:

* **Cadence<->Server**: Inter-process communication (IPC). The server is invoked by Cadence and waits for a client communication.
* **Client<->Server**: Python sockets (more info `here <https://docs.python.org/3.6/library/socket.html>`_). Both processes can be run on the same machine or on different machines, according to the socket type chosen by the user. TCP sockets are used by default.

By using this library it is possible to control the Cadence environment from an external program. 

This project code is available on **Github** at https://github.com/mdmfernandes/socad.

* :doc:`installation`
* :doc:`usage`
* :doc:`api/index`
* **Tutorials**
    * :doc:`tutorials/basic_communication`
    * :doc:`tutorials/common_source`
* :doc:`contributing`
* :doc:`about`

.. toctree::
   :hidden:
   
   installation
   usage
   api/index
   tutorials/basic_communication
   tutorials/common_source
   contributing
   about