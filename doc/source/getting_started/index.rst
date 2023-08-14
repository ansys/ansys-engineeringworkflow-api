Getting started
===============

Installation
------------

Two installation modes of the ``ansys-engineeringworkflow-api`` package are provided: user and developer.

User installation
^^^^^^^^^^^^^^^^^

Install the latest release for use with this command:

.. code:: bash

    python -m pip install ansys-engineeringworkflow-api


For developers
^^^^^^^^^^^^^^

Installing the ``ansys-engineeringworkflow-api`` package in developer mode allows
you to modify the source and enhance it.

You can refer to the :ref:`ref_contribute` section.

Style and testing
-----------------

If required, you can call style commands (such as `black`_, `isort`_,
and `flake8`_) or unit testing commands (such as `pytest`_) from the command line.
However, this does not guarantee that your project is being tested in an isolated
environment, which is why you might consider using `tox`_.


Documentation
-------------

For building documentation, you can run the usual rules provided in the
`Sphinx`_ Makefile:

.. code:: bash

    python -m pip install .[doc]
    make -C doc/ html

    # subsequently open the documentation with (under Linux):
    your_browser_name doc/html/index.html

Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements:

.. code:: bash

    python -m pip install -e .[doc,tests]

Then, execute these commands:

    .. code:: bash

        python -m build
        python -m twine check dist/*
