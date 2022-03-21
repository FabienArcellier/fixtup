Installation
############

The installation of ``Fixtup`` is done with ``pip``.

.. code-block:: bash

    pip install fixtup

.. note::

    If you manage your dependencies through ``setup.py``, ``setup.cfg``, ``pyproject.toml``, ``pipenv`` or ``poetry``,
    you should declare and install ``fixtup`` as a dev dependencies.

.. _ConfigureFixtup:

Configure fixtup
****************

To be able to use ``Fixtup``, you must initialize and declare a fixture repository. It's a folder
which will contain all the fixtures for your python project.

.. note::

    This step is required to be able to use the command line ``fixtup``

Configure fixtup with setup.cfg
===============================

The first way to configure ``Fixtup`` is to add a section `fixtup`
in the ``setup.cfg`` manifest of your python project.

.. code-block:: ini
    :caption: ./setup.cfg

    [fixtup]
    fixtures=tests/fixtures
    plugins=
        fixtup.plugins.docker
        fixtup.plugins.dotenv

.. note::

    ``Fixtup`` crawls through your project tree to find python manifest
    ``setup.cfg`` or ``pyproject.toml``.

Configure fixture with pyproject.toml
=====================================

Another way to configure ``Fixtup`` is to add a ``tools.fixtup`` section in
the ``pyproject.toml`` manifest of your python project.

.. code-block:: ini
    :caption: ./pyproject.toml

    [tools.fixtup]
    fixtures=tests/fixtures
    plugins=[
        "fixtup.plugins.docker",
        "fixtup.plugins.dotenv"
    ]


Configure fixtup as a module
============================

You can also declare the fixtup path in a python module that will be included in your test suite.

.. warning::

    This method is not recommended. You won't be able to use the command line to create your new fixtures.
    However, it allows to have several fixtures repositories in your code base.


.. code-block:: python
    :caption: ./tests/units/__init__.py

    import os

    import fixtup

    SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
    fixtup.configure({"fixtures": os.path.join(SCRIPT_DIR, "../fixtures")})

