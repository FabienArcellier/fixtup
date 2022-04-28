Handbook
########

``Fixtup`` presents itself as a toolkit for managing and customizing environments
to run your tests and improve your Quality Assurance process.

.. contents::
  :backlinks: top
  :local:

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
    :caption: tests/fixtures/database_context/.hooks/hook_started.py

    import fixtup

    fixtup.helper.wait_port(5432, timeout=2000)


Configure environnement variables dedicated to the fixture
**********************************************************

Les variables d'environnments offrent un moyen de spécifier la configuration à adopter au runtime.
``Fixtup`` permet de les spécifier dans votre fixture au moyen d'un fichier ``.env``. Les variables de ce fichier
seront chargées au moment où la fixture démarre.

C'est le bon endroit pour passer une ressource partagée pour les tests automatique, par exemple l'adresse d'un bucket S3
qui stocke des fichiers temporaires que manipule votre application.

Mount a fixture once and keep it mounted for all the tests
**********************************************************

When the `keep_mounted` policy is active on a fixture, it is mounted only once at the first test that use this fixture,
then reused by each test. Between each test the fixture is starting and stopping. For exemple, with the docker
plugin, network is mounted only once. Containers start and stop between every tests.

.. warning:: If you persist information in your test, like create a file or add record in a database, they will be
    present when fixtup will be running the next test that use this fixture.

When the test runtime stop or when the user interrupts the tests, the fixture is unmounted.

To enable the `keep_mounted` policy, edit `fixtup.yml` in a fixture template

.. code-block:: yaml
    :caption: tests/fixtures/fixtup/simple_fixture/fixtup.yml

    keep_mounted: true

Keep a fixture running for all the tests
****************************************

Sometimes, the fixture is slow to start and stop. In that case, you want to keep the fixture mounted and running
during all your tests. You want to avoid the fixture to start and stop on every test.

The ``keep_running`` policy allows you to do this. Once the fixture is mounted, it will remain up during all tests.
For example, if your fixture mounts a postgresql database, the database will stay up and running between all your
tests.

.. code-block:: yaml
    :caption: ./tests/fixtures/postgres_datastore/fixtup.yml

    keep_running: true

.. warning:: You cannot use 2 postgresql databases on the same port in 2 different fixtures
    if you are using a fixture with the ``keep_running`` policy.


.. warning:: There is no hook yet in fixtup for execute a code and load / clean data for example between 2 tests on a
    fixture with ``keep_running`` policy.

more about :term:`fixture livecycle`

.. _HookWaitAvailability:

Wait for the availability of a service in a fixture
***************************************************

The following example waits for port 5432 to respond on a postgresql dtabase. It uses the ``hook_started.py`` hook.
The call to ``fixtup.helper.wait_port`` is blocking. As long as port 5432 does not respond,
your test will not start. If a timeout occurs, your test fails.

.. code-block:: python
    :caption: tests/fixtures/simple_postgresql/.hooks/hook_started.py

    import fixtup

    fixtup.helper.wait_port(5432, timeout=2000)

more about :term:`fixture hook`

.. _HookLoadData:

Load data when starting a fixture
*********************************

You can use ``sqlalchemy`` in a hook to bootstrap the schema of sqlalchemy and mount
data inside a ``sqlalchemy`` managed database as ``sqlite`` and ``postgres``.

.. code-block:: python
    :caption: tests/fixtures/simple_board/.hooks/hook_started.py

    import kanban.database
    from kanban.model import BoardColumn, WorkItem

    kanban.database.db_init()
    dbsession = kanban.database.db_session()

    dbsession.add(BoardColumn(pid=1, step_name="TODO", wip_limit=None))
    dbsession.add(BoardColumn(pid=2, step_name="DOING", wip_limit=4))
    dbsession.add(BoardColumn(pid=3, step_name="DONE", wip_limit=None))
    dbsession.commit()

    dbsession.add(WorkItem(pid=1, title='implement feature AAA', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
    dbsession.add(WorkItem(pid=2, title='implement feature BBB', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
    dbsession.add(WorkItem(pid=3, title='implement feature CCC', column=3, description='xxxxxxxxxxxxxxxxxxxx'))
    dbsession.add(WorkItem(pid=12, title='implement feature XXX', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
    dbsession.commit()


`A working example is present in fixtup repository <https://github.com/FabienArcellier/fixtup/tree/master/examples/kanban_flask_sqlite>`__.

more about :term:`fixture hook`

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
