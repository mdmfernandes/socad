Installation
============

Requirements
------------

Both **client** and **server** are written in Python 3.6. However, both modules are compatible with Python 2.7 and the **server** was also tested in Python 2.6.

Install with *pip*
------------------

Although the project is not in PyPI, you can install it using *pip*. Go to the project folder and run:

.. code-block:: shell

    pip install .


**NOTE:** run ``pip install socad`` from the project directory doesn't work because pip will look for the package on PyPi.

Build from source
-----------------

Go to the project folder and run:

.. code-block:: shell

    python setup.py install


Use as local module
-------------------

For the provided example, if the Cadence machine does not allow to install the **socad** package from the methods above, the module is loaded from ``examples/socad_cadence/server.py``.
