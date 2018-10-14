# SOCAD

Connect Cadence Virtuoso to a Python client using sockets.

## Installation

The installation needs to be performed both in the **client** and the **server**. We recommend you to use *easy_install* or *pip* to install SOCAD in your system.

### Install with *pip*

Go to the project folder and run:

```shell
pip install .
```

**NOTE:** run `pip install socad` from the project directory doesn't work because pip will look for the package on PyPi.

### Build from source

Go to the project folder and run:

```shell
python setup.py install
```

### Use local module

If the Cadence machine does not allow to install the **socad** package from the methods above, it loads the module from `examples/socad_cadence/server.py`.

## Usage

Import the *Client* or the *Server* to your program using:

```python
from socad import Client
from socad import Server
```

TODO: Complete

## Example

The provided example emulates the execution of a program that runs simulations in Cadence Virtuoso from a client in a different machine (connected through *ssh*), by executing OCEAN scripts that are provided by the user.

To run the example:

1. Place the package **example/socad_cadence/** in the machine that runs Cadence (i.e. the **server**).
2. Place the package **example/** in your computer.
3. Connect your computer to the **server**. If you are connect through ssh you need to set a local forwarding for the port used to perform communication. E.g.:

```Shell script
ssh -L LOCAL_PORT:localhost:HOST_PORT user@SERVER_IP
```

4. Run Cadence, in the **server**, by executing the script *start_cadence.sh*.
5. Run *socad_example.py* on your computer.

The following menu should appear at the program execution:

```text
############### SOCAD EXAMPLE ###############
1 - Load simulator
2 - Update variables and run simulation
0 - Exit.
```

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
