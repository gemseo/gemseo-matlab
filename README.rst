MATLAB wrapper for GEMSEO

Documentation
-------------

Currently, the documentation of this plugin is available via the documentation of GEMSEO.

Installation
~~~~~~~~~~~~

Executing a MATLAB discipline requires that a MATLAB
engine as well as its Python API are installed.
The MATLAB Python API is not defined as a dependency of this package,
because until MATLAB release R2020b there was no package available in PyPI.
It shall be installed in the same environment as the one in which this plugin is installed,
please refer to the MATLAB documentation to install it.
To make sure that MATLAB works fine through the Python API,
start a Python interpreter and
check that there is no error when executing :code:`import matlab`.

Development
~~~~~~~~~~~

For testing with ``tox``,
set the environment variable :envvar:`MATLAB_PYTHON_WRAPPER`
to point to the URL or path of a ``pip`` installable version of the MATLAB Python API,
with eventually a conditional dependency on the Python version:

.. code-block:: console

   export MATLAB_PYTHON_WRAPPER="<path or URL to MATLAB Python API package> ; python_version<'3.9'"


Bugs/Questions
--------------

How to report bugs?

License
-------

What is the license?

Contributors
------------

- GEMSEO developers
