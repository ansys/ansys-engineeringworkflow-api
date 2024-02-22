Ansys Engineering Workflow API
==============================

Overview
--------
The Ansys Engineering Workflow API is a Python package that provides a
common interface for interacting with Ansys engineering workflow engines,
such as ModelCenter and OptiSLang.


Installation
------------
The ``ansys-engineeringworkflow-api`` package currently supports Python
3.9 through 3.12 on Windows, MacOS and Linux.

You can install ``ansys-engineeringworkflow-api`` with:

.. code::

   pip install ansys-engineeringworkflow-api

Alternatively, install the latest version from `ansys-engineeringworkflow-api GitHub
<https://github.com/ansys/ansys-engineeringworkflow-api>`_ via:

.. code::

   pip install git+https://github.com/ansys/ansys-engineeringworkflow-api


For a local development version, you can install the development
version of the project with:

.. code::

   git clone https://github.com/ansys/ansys-engineeringworkflow-api.git
   cd ansys-engineeringworkflow-api
   pip install -e .


Documentation building
----------------------

Install the required dependencies for building the documentation with this
command:

.. code:: bash

    pip install .[doc]

Build and view documentation with the one or more commands for your
operating system:

.. code:: bash

    # For Linux and MacOS
    make -C doc/ html && your_browser_name doc/build/html/index.html

    # For Windows
    .\doc\make.bat html
    .\doc\build\html\index.html
