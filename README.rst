..
    Copyright 2021 IRT Saint Exupéry, https://www.irt-saintexupery.com

    This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
    International License. To view a copy of this license, visit
    http://creativecommons.org/licenses/by-sa/4.0/ or send a letter to Creative
    Commons, PO Box 1866, Mountain View, CA 94042, USA.

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
set the environment variable :envvar:`MATLAB_PIP_REQ_SPEC`
to point to the URL or path of a ``pip`` installable version of the MATLAB Python API,
with eventually a conditional dependency on the Python version:

.. code-block:: console

   export MATLAB_PIP_REQ_SPEC="matlabengine==X.Y.Z"

Docker
~~~~~~

To create or update the podman/docker images for testing the plugin,
adapt with the proper version of matlab:

.. code-block:: console

   podman build Dockerfile -t gemseo-matlab:r2020b --build-arg=MATLAB_VERSION=r2020b


Bugs/Questions
--------------

Please use the gitlab issue tracker at
https://gitlab.com/gemseo/dev/gemseo-matlab/-/issues
to submit bugs or questions.

License
-------

The GEMSEO-MATLAB source code is distributed under the GNU LGPL v3.0 license.
A copy of it can be found in the LICENSE.txt file.
The GNU LGPL v3.0 license is an exception to the GNU GPL v3.0 license.
A copy of the GNU GPL v3.0 license can be found in the LICENSES folder.

The GEMSEO-MATLAB examples are distributed under the BSD 0-Clause, a permissive
license that allows to copy paste the code of examples without preserving the
copyright mentions.

The GEMSEO-MATLAB documentation is distributed under the CC BY-SA 4.0 license.

The GEMSEO-MATLAB product depends on other software which have various licenses.
The list of dependencies with their licenses is given in the CREDITS.rst file.

Contributors
------------

- GEMSEO developers
