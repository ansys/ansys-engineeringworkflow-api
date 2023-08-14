Engineering Workflow API
########################

Project Overview
----------------
Provide a description of your PyAnsys Python library.


Installation
------------

You can install the ``ansys-engineeringworkflow-api`` library with:

.. code::

   pip install ansys-engineeringworkflow-api

Alternatively, clone and install in development mode with:

.. code::

   git clone https://github.com/ansys/ansys-engineeringworkflow-api
   cd ansys-engineeringworkflow-api
   python -m venv .venv

This creates a new virtual environment, which can be activated with

.. code::

	.\.venv\Scripts\activate


Installation
------------
The ``ansys-engineeringworkflow-api`` package currently supports Python
3.8 through 3.11 on Windows, MacOS and Linux.

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

   git clone https://github.com/pyansys/pyansys-tools-variableinterop.git
   cd pyansys-tools-variableinterop
   pip install -e .


Documentation
-------------

Install the required dependencies for the documentation with:

.. code:: bash

    pip install .[doc]

    # For Linux and MacOS
    make -C doc/ html && your_browser_name doc/build/html/index.html

    # For Windows
    .\doc\make.bat html
    .\doc\build\html\index.html

TODO
-------
  	- [ ] Finish documentation such that pre-commit works as intended
	- [ ] Copy (manually, automatically?) main package documentation to README
	- [ ] To/FromAPI String
		- No extension methods in Python, add to base interface explicitly?
		- Our string quoting rules per standard doc (Phoenix.ModelCenter.Common.ModelCenterUtils.EscapeString and UnescapeString)
	- [ ] To/From Formatted String
	- [ ] Scalar Types
	- [ ] Array Types
		- Strong typing of ndarray in numpy only added in version of numpy that doesn't support Python 3.7
	- [ ] File Types
		- Use interface to separate behavior of files from library
		- Implement default behavior
	- [ ] Clone
	- [ ] LinkingRules
	- [ ] Variable Factory
	- [ ] Variable State
	- [ ] Variable Scope
