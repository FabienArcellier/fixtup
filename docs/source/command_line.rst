.. _CommandLine:

Command line
############

The ``fixtup`` command line tool is an assistant to configure your python project and manage the existing fixtures.
You can invoke it in your shell, once you have activated the virtual environment in
which you installed fixtup.

.. contents::
    :backlinks: top
    :local:

``fixtup init`` - install fixtup in a python project
****************************************************


The ``fixtup init`` command initiates your fixture repository and configures the python manifest.

.. code-block:: bash

    $ fixtup init

    Choose a directory to store fixture templates : tests/fixtures
    Python manifest (setup.cfg/pyproject.toml) [setup.cfg]

``fixtup new`` - generate a new fixture
***************************************

The ``fixtup new`` command generates a new fixture in your fixture repository.
This command creates the folder for you, instantiates hooks, initiates artifacts
required by plug-ins.

In less than 2 minutes you are ready to use fixtup in your project.

.. code-block::

    $ fixtup new

    Choose a fixture identifier : thumbnail_context
    Mount environment variables on this fixture (y/n) [y]
    Mount docker container on this fixture (y/n) [y]

The result will take this form in ``tests/fixture/fixtup/simple``

.. code-block::
    :caption: tests/fixture/fixtup/simple

    .
    ├── docker-compose.yml
    ├── fixtup.yml
    └── .hooks
        ├── hook_mounted.py.sample
        ├── hook_started.py.sample
        ├── hook_stopped.py.sample
        └── hook_unmounted.py.sample

``fixtup info`` - view configuration information
************************************************

The `fixtup info` command displays a summary of important parameters such as
the file that contains the fixtup configuration or the repository that contains the fixture templates.

.. code-block:: bash

    $ fixtup info

    Configuration: /home/far/documents/project/setup.cfg
    Fixtures: /home/far/documents/project/tests/fixtures/fixtup
    Plugins:
        * fixtup.plugins.dotenv
        * fixtup.plugins.docker


