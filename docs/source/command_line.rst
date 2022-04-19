Command line
############

The ``fixtup`` command line tool is an assistant to configure your python project and manage the existing fixtures.
You can invoke it in your shell, once you have activated the virtual environment in
which you installed fixtup.

Activate fixtup in a python project
***********************************


The ``fixtup init`` command initiates your fixture repository and configures the python manifest.

.. code-block:: bash

    $ fixtup init

    Fixture repository ? tests/fixtures/fixtup
    Manifest ? pyproject.toml

Generate a new fixture
**********************

The ``fixtup new`` command generates a new fixture in your fixture repository.
This command creates the folder for you, instantiates hooks, initiates artifacts
required by plug-ins.

In less than 2 minutes you are ready to use fixtup in your project.

.. code-block::

    $ fixtup new

    Fixture directory ? simple
    Is this fixture is shared between all the tests ? no
    Is this fixture use docker container ? yes
    Is this fixture use .env file ? no

The result will take this form in ``tests/fixture/fixtup/simple``

.. code-block::
    :caption: tests/fixture/fixtup/simple

    .
    ├── docker-compose.yml
    └── .hooks
        ├── hook_mounted.py.sample
        ├── hook_started.py.sample
        ├── hook_stopped.py.sample
        └── hook_unmounted.py.sample

Afficher les informations relatives à la configuration
******************************************************

La commande `fixtup info` vous permet d'avoir une vue de la configuration active. Elle affiche
une synthèse des paramètres importants comme le fichier qui contient la configuration de fixtup ou
le repository qui contient les templates de fixture.

.. code-block:: bash

    $ fixtup info

    Configuration: /home/far/documents/project/setup.cfg
    Fixtures: /home/far/documents/project/tests/fixtures/fixtup
    Plugins:
        * fixtup.plugins.dotenv
        * fixtup.plugins.docker


