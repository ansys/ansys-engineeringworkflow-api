PyAnsys Library Template
########################

This repository is a template repository where you can `Create a
repository from a template`_ and create a new PyAnsys project that
follows the guidelines specified in the `PyAnsys Developer's Guide`_.

The following sections should be filled and documented for your project.

.. _Create a repository from a template: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template
.. _PyAnsys Developer's Guide: https://github.com/pyansys/about


Project Overview
----------------
Provide a description of your PyAnsys Python library.


Installation
------------
Include installation directions.  Note that this README will be
included in your PyPI package, so be sure to include ``pip``
directions along with developer installation directions.  For example.

Install <PyAnsys Library> with:

.. code::

   pip install ansys-<product/service>-<library>

Alternatively, clone and install in development mode with:

.. code::

   git clone https://github.com/pyansys/
   cd <PyAnsys-Library>
   pip install poetry
   poetry install

This creates a new virtual environment, which can be activated with

.. code::

   poetry shell

A third alternative is to use DevContainers, either from the cli or
with Visual Studio Code. Install VS Code and the Dev Extensions plug-in,
then use `Dev Containers: Open Folder in Container`. The `poetry install`
should happen for you.

Documentation
-------------
Include a link to the full sphinx documentation.  For example `PyAnsys <https://docs.pyansys.com/>`_


Usage
-----
It's best to provide a sample code or even a figure demonstrating the usage of your library.  For example:

.. code:: python

   >>> from ansys.<product/service> import <library>
   >>> my_object.<library>()
   >>> my_object.foo()
   'bar'


Testing
-------
You can feel free to include this at the README level or in CONTRIBUTING.md


License
-------
Be sure to point out your license (and any acknowledgments).  State
that the full license can be found in the root directory of the
repository.


TODO
-------
	- Finish documentation such that pre-commit works as intended
	- Copy (manually, automatically?) main package documentation to README
	- To/FromAPI String
		- No extension methods in Python, add to base interface explicitly?
		- Our string quoting rules per standard doc (Phoenix.ModelCenter.Common.ModelCenterUtils.EscapeString and UnescapeString)
	- To/From Formatted String
	- Scalar Types
	- Array Types
		- Strong typing of ndarray in numpy only added in version of numpy that doesn't support Python 3.7
	- File Types
		- Use interface to separate behavior of files from library
		- Implement default behavior
	- Clone
	- LinkingRules
	- Variable Factory
	- Variable State
	- Variable Scope
