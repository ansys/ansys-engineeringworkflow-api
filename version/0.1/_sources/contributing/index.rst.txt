.. _ref_contribute:

Contribute
==========

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys developer's guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to the Ansys Engineering Workflow API.

The following contribution information is specific to the Ansys Engineering Workflow API.

Install in developer mode
-------------------------

Installing the ``ansys-engineeringworkflow-api`` package in developer mode allows
you to modify the source and enhance it. This package supports Python 3.9 through 3.12
on Windows, MacOS, and Linux.

For a local development version, you can create a clean virtual environment with this command:

.. code:: bash

    python -m venv .venv

You can then activate this virtual environment with the command appropriate for your operating system:

.. tab-set::

      .. tab-item:: Linux
        :sync: linux

        ::

          source .venv/bin/activate

      .. tab-item:: macOS
        :sync: macos

        ::

          source .venv/bin/activate

      .. tab-item:: Windows
        :sync: windows

        ::

          .\.venv\Scripts\activate


Next, install the development version of the ``ansys-engineeringworkflow-api`` package
with these commands:

.. code::

   git clone https://github.com/ansys/ansys-engineeringworkflow-api
   cd ansys-engineeringworkflow-api
   pip install -e .


Build documentation
-------------------

Install the required dependencies for the documentation with this command:

.. code::

    pip install .[doc]


To build documentation, run the usual rules provided in the Sphinx
Makefile for your operating system:

.. tab-set::

    .. tab-item:: Linux
      :sync: linux

      ::

        make -C doc/ html && your_browser_name doc/build/html/index.html

    .. tab-item:: macOS
      :sync: macos

      ::

        make -C doc/ html && your_browser_name doc/build/html/index.html

    .. tab-item:: Windows
      :sync: windows

      ::

        .\doc\make.bat html
        .\doc\build\html\index.html

Post issues
-----------

Use the `Ansys Engineering Workflow API Issues <ansys-engineeringworkflow-api_issues_>`_
page to report bugs and request new features.

When possible, use the issue templates provided. If your issue does not fit into one
of the templates, you can click the link for opening a blank issue.

To reach the PyAnsys support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

Verify style and unit tests
---------------------------

If required, from the command line, you can call commands like `black`_, `isort`_, and `flake8`_.
You can also call unit testing commands like `pytest`_. However, running these commands does not
guarantee that your project is being tested in an isolated environment, which is why you
might consider using `tox`_.

Test
----
You can install the dependencies required for testing with this command:

.. code:: bash

    pip install .[tests]

You can then run the tests via ``pytest`` with this command:

.. code:: bash

    pytest -v


Adhere to code style
--------------------

The Ansys Engineering Workflow API follows the PEP8 standard as indicated in the 
`PyAnsys developer's guide <dev_guide_pyansys_pep8_>`_ and implements style checking using
`pre-commit <pre-commit_>`_.

To ensure your code meets minimum code styling standards, run these commands:

.. code:: console

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command:

.. code:: console

  pre-commit install


This way, it's not possible for you to push code that fails the style checks:

.. code:: text

  $ git commit -am "added my cool feature"
  Add License Headers......................................................Passed
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  docformatter.............................................................Passed
  codespell................................................................Passed
  Validate GitHub Workflows................................................Passed

Distribute
----------

If you would like to create either source or wheel files, start by running this
command to install the building requirements:

.. code:: bash

    python -m pip install -e .[doc,tests]

Then, run these commands:

.. code:: bash

    python -m build
    python -m twine check dist/*
