Installation
############

The installation of ``Fixtup`` is done with ``pip``.

.. code-block:: bash

    pip install fixtup

.. note::

    If you manage your dependencies through ``setup.py``, ``setup.cfg``, ``pyproject.toml``, ``pipenv`` or ``poetry``,
    you should declare and install ``fixtup`` as a dev dependencies.

.. _ConfigureFixtup:

Configure fixtup on your project
********************************

To be able to use ``Fixtup``, you must initialize it in your python project.
Fixtup can do that for you with the command

.. code-block:: bash

    fixtup init

.. warning:: If you haven't manifest for your project, you should declare one.

    You will need a `pyproject.toml` which declares you want to use setuptools to package your project.

    .. code-block::
        :caption: ./pyproject.toml

        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"

    * `more information in setuptools tutorial <https://setuptools.pypa.io/en/latest/userguide/quickstart.html#basic-use>`__
    * `understanding setup.py, setup.cfg and pyproject.toml in Python <https://ianhopkinson.org.uk/2022/02/understanding-setup-py-setup-cfg-and-pyproject-toml-in-python/>`__
    * `Alice in python project land <https://vickiboykis.com/2017/09/26/alice-in-python-projectland/>`__

If you want to configure ``Fixtup`` all by yourself, look at the section relative to your project manifest.

.. contents::
    :local:

Configure fixtup with setup.cfg
===============================

The first way to configure ``Fixtup`` is to add a section `fixtup`
in the ``setup.cfg`` manifest of your python project.

.. code-block:: ini
    :caption: ./setup.cfg

    [fixtup]
    fixtures=tests/fixtures
    plugins=
        fixtup.plugins.dotenv
        fixtup.plugins.docker

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
        "fixtup.plugins.dotenv",
        "fixtup.plugins.docker"
    ]


Configure fixtup as a module
============================

You can also declare the fixtup path in a python module that will be included in your test suite.

.. warning::

    This method is not recommended. You won't be able to use the command line to create your new fixtures.
    However, it allows to have several fixtures repositories in your code base.


.. code-block:: python
    :caption: ./tests/units/conftest.py

    import os

    import fixtup

    SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
    fixtup.configure({"fixtures": os.path.join(SCRIPT_DIR, "../fixtures")})

