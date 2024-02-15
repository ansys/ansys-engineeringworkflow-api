Getting started
===============

Installation
------------

Two installation modes of the ``ansys-engineeringworkflow-api`` package are provided: user and developer.

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing the ``ansys-engineeringworkflow-api`` package, make sure that you
have the latest version of `pip`_ with this command:

.. code:: bash

    python -m pip install -U pip

Then, install the latest ``ansys-engineeringworkflow-api`` package with this command:

.. code:: bash

    python -m pip install ansys-engineeringworkflow-api

Install in developer mode
^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the ``ansys-engineeringworkflow-api`` package in developer mode allows
you to modify the source and enhance it.
For more information, see :ref:`ref_contribute`.

Style and testing
-----------------

If required, you can call style commands (such as `black`_, `isort`_,
and `flake8`_) or unit testing commands (such as `pytest`_) from the command line.
However, this does not guarantee that your project is being tested in an isolated
environment, which is why you might consider using `tox`_.


Distributing
------------

If you would like to create either source or wheel files, start by running this
command to install the building requirements:

.. code:: bash

    python -m pip install -e .[doc,tests]

Then, run these commands:

.. code:: bash

    python -m build
    python -m twine check dist/*
