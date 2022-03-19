Handbook
########

``Fixtup`` presents itself as a toolkit for managing and customizing environments
to run your tests and improve your Quality Assurance process.

.. contents::
  :backlinks: top

Build a postgresql database in a fixture
****************************************

Using the docker plugin (present by default), a fixture can declare service to start when the fixture is mounted.
This declaration is a ``docker-compose.yml`` file at the root of the fixture.

When the test starts, the fixture will run the containers from the working directory
mounted from the fixture.

.. code-block:: text

        .
    ├── pyproject.toml
    ├── setup.cfg
    └── tests
        └── fixtures
            └── database_context
                ├── docker-compose.yml
                ├── fixtup.yml
                └── .hooks
                    ├── hook_mounted.py.sample
                    ├── hook_started.py
                    ├── hook_stopped.py.sample
                    └── hook_unmounted.py.sample

To emulate postgresql, you declare the container in the ``docker-compose.yml`` file.

.. code-block:: yaml
    :caption: tests/fixtures/database_context/docker-compose.yml

    version: '3'
    services:
      postgresql:
        image: postgres
        ports:
          - "5432:5432"
        environment:
          - POSTGRES_PASSWORD=1234

The loading of the container may take some time. Instead of waiting the container to be ready in your own
test, ``Fixtup`` gives you a way to implement a hook called on the fixture has been started.

This hook allow you to wait the availability of the port 5432, the port of the postgresql database.

.. code-block:: python
    :caption: tests/fixtures/database_context/.hooks/started.py

    import fixtup

    fixtup.helper.wait_port(5432, timeout=2000)


Configure environnement variables dedicated to the fixture
**********************************************************

Les variables d'environnments offrent un moyen de spécifier la configuration à adopter au runtime.
``Fixtup`` permet de les spécifier dans votre fixture au moyen d'un fichier ``.env``. Les variables de ce fichier
seront chargées au moment où la fixture démarre.

C'est le bon endroit pour passer une ressource partagée pour les tests automatique, par exemple l'adresse d'un bucket S3
qui stocke des fichiers temporaires que manipule votre application.

Mount a fixture once for several tests
**************************************

Implement your own processing on a fixture event
************************************************

Un environnement décrit par une fixture peut prendre du temps à être opérationnel.
Fixtup permet grâce à des hooks d'exécuter du code à vous pour attendre qu'un socket soit ouvert, pour charger des données,
ou attendre que la sonde de readiness d'un container docker soit prête ...

Les hooks s'implémentent dans des modules python. Vous allez les écrire dans le dossier
``.hooks`` à l'intérieur de chacune de vos fixtures. Les hooks sont optionnels.

L'exemple qui suit attends que le port 5432 réponde sur une base postgresql. L'appel à ``fixtup.helper.wait_port`` est
bloquant. Tant que le port 5432 ne réponds pas, votre test ne démarrera pas. En cas de timeout, votre test échoue.

.. code-block:: python
    :caption: tests/fixtures/simple_postgresql/.hooks/hook_started.py

    import fixtup

    fixtup.helper.wait_port(5432, timeout=2000)

Fixtup propose 4 hooks.

* ``hook_mounted.py`` : exécuté lorsque la fixture est montée, c'est à dire que le dossier de la fixture est copié
* ``hook_started.py`` : exécuté lorsque la fixture est démarrée, par exemple après que docker-compose se soit exécuté et après le chargement
    des variables d'environnement
* ``hook_stopped.py`` : exécuté lorsque la fixture est arrêtée
* ``hook_unmounted.py`` : exécuté lorsque le dossier qui contient la fixture est effacée

Use Fixtup with other test frameworks
*************************************

``Fixtup`` is agnostic to the testing framework. You should be able to use it with
other frameworks like `robotframework <https://robotframework.org/>`__, ...

Debug the result of a test by keeping the mounted fixture
*********************************************************

At the end of the tests, whatever the fixtup policities, mounted fixtures are cleanup. In some case, you want to
keep some of them to debug what has been done inside.

You should use the flag `keep_mounted_fixture` to keep them in the tmp directory. You will be able to
explore what is inside the directories of mounted fixtures and even run the artefact manage by fixtup plugins that
are not clean up as well (containers for example, ...).

.. code-block:: python
    :caption: ./tests/integrations/test_utils.py

    import unittest
    import os

    import fixtup

    class UtilsTest(unittest.TestCase)

        def test_thumbnail_should_generate_thumbnail(self):
            with fixtup.up('thumbnail_context', keep_mounted_fixture=True):
                # Given
                wd = os.getcwd()

                # ...
