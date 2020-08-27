# SOCAD

Client: [![Python -V client](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/release/python-360/)
Server: [![Python -V server](https://img.shields.io/badge/python-2.6%2B-blue.svg)](https://www.python.org/downloads/release/python-260/) [![Documentation Status](https://readthedocs.org/projects/socad/badge/?version=latest)](https://socad.readthedocs.io/en/latest/?badge=latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://github.com/mdmfernandes/socad/blob/master/LICENSE)

## This project is no longer maintained, as I no longer have access to Cadence Virtuoso. If you are interested in contributing and have any questions, feel free to contact me.

**SOCAD** connects Cadence Virtuoso to a Python client. The communication between both processes is made through a server, using the following mechanisms:

* **Cadence<->Server**: Inter-process communication (IPC). The server is invoked by Cadence and waits for a client communication.
* **Client<->Server**: Sockets (more info [here](https://docs.python.org/3/library/socket.html)). Both processes can be run on the same machine or on different machines, according to the socket type chosen by the user. TCP sockets are used by default.

By using this library it is possible to control the Cadence environment from an external program.

## Installation

The installation needs to be performed both in the **client** and the **server**. We recommend you to use *pip* to install SOCAD in your system.

### Install with *pip*

Although the project is not in PyPI, you can install it using *pip*. Go to the project folder and run:

```shell
pip install .
```

**NOTE:** run `pip install socad` from the project directory doesn't work because pip will look for the package on PyPi.

### Build from source

Go to the project folder and run:

```shell
python setup.py install
```

### Use as local module

If the Cadence machine does not allow to install the **socad** package from the methods above, the module is loaded from `examples/socad_cadence/server.py`.

## Usage

Import the *Client* or the *Server* to your program using:

```python
from socad import Client
from socad import Server
```

The available functions of each class are available in the project [library reference](https://socad.readthedocs.io/en/latest/api/index.html).

A complete demonstration of the program usage can be found in the example below.

## Example

The provided example runs simulations in Cadence Virtuoso from a client in a different machine (connected through *ssh*), by executing OCEAN scripts provided by the user.

For more a step by step guide of the example, check [this tutorial](https://socad.readthedocs.io/en/latest/tutorials/common_source.html).

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [releases on the project repository](https://github.com/mdmfernandes/socad/releases/).

## Main Contributors

* **Miguel Fernandes** - *Initial work* - [mdmfernandes](https://github.com/mdmfernandes)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

This project is licensed under the GPLv3 License - see the project [LICENSE](https://github.com/mdmfernandes/socad/blob/master/LICENSE) file for details.
