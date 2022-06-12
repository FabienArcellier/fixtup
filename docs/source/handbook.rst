Handbook
########

``Fixtup`` presents itself as a toolkit for managing and customizing environments
to run your tests and improve your Quality Assurance process.

.. contents::
  :backlinks: top
  :local:

Mount a postgresql database in a test
*************************************

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
        mydb:
            image: postgres
            ports:
                - "5432:5432"
            environment:
                - POSTGRES_PASSWORD=1234
            volumes:
                - ./docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d

The loading of the container may take some time. Instead of waiting the container to be ready in your own test, ``Fixtup`` gives you a way to implement a hook called on the fixture has been started.

This hook allow you to wait the availability of the port 5432, the port of the postgresql database.

.. code-block:: python
    :caption: tests/fixtures/database_context/.hooks/hook_started.py

    import fixtup

    fixtup.helper.wait_port(5432, timeout=2000)


.. note::

    more about :ref:`plugins_docker`

Override environnement variables in a test
******************************************

Environment variables are the way to specify the configuration to adopt at runtime in a `twelve factor architecture <https://12factor.net/>`__.

When the ``fixtup.plugins.env`` plugin is active, you can overridde or add any variable through a ``.env`` file in the
fixture template directory.

.. code-block:: bash
    :caption: tests/fixtures/database_context/.env

    # describe the environment variables you want
    # load on test start
    #
    # the original environment is restored
    # when the test ends
    #
    # VAR1="HELLO"
    TMP_DIRECTORY=/tmp

.. note::

    more about :ref:`plugins_dotenv`

Keep a fixture running between the tests
****************************************

The ``keep_running`` policy keeps the environment loaded after the fixture is used, until the test runner stops. Once the fixture is started, it will remain up during all tests.

This policy is useful when the docker stack takes too much time to start and stop. We will reuse this stack between all our tests. For example, if your fixture mounts a postgresql database, the database will stay up and running between all your tests.

.. code-block:: yaml
    :caption: ./tests/fixtures/postgres_datastore/fixtup.yml

    keep_running: true

.. warning:: You cannot use 2 postgresql databases on the same port in 2 different fixtures
    if you are using a fixture with the ``keep_running`` policy.

.. note::

    more about :term:`fixture livecycle`

.. _HookWaitAvailability:

Wait for the availability of a service before running a test
************************************************************

The following example waits for port 5432 to respond on a postgresql dtabase. It uses the ``hook_started.py`` hook. The call to ``fixtup.helper.wait_port`` is blocking. As long as port 5432 does not respond, your test will not start. If a timeout occurs, your test fails.

.. code-block:: python
    :caption: tests/fixtures/simple_postgresql/.hooks/hook_started.py

    import fixtup

    fixtup.helper.wait_port(5432, timeout=2000)

.. note::

    more about :term:`fixture hook`

.. _HookLoadData:

Populate a database with data before running a test
***************************************************

You can use ``sqlalchemy`` in a hook to bootstrap the schema of sqlalchemy and mount
data inside a ``sqlalchemy`` managed database as ``sqlite`` and ``postgres``.

Le hook ``hook_setup_data`` est exécuté avant de jouer le test.

.. code-block:: python
    :caption: tests/fixtures/simple_board/.hooks/hook_setup_data.py

    import kanban.database
    from kanban.database import db_session
    from kanban.model import BoardColumn, WorkItem

    kanban.database.reset_db()

    db_session.add(BoardColumn(pid=1, step_name="TODO", wip_limit=None))
    db_session.add(BoardColumn(pid=2, step_name="DOING", wip_limit=4))
    db_session.add(BoardColumn(pid=3, step_name="DONE", wip_limit=None))
    db_session.commit()

    db_session.add(WorkItem(pid=1, title='implement feature AAA', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
    db_session.add(WorkItem(pid=2, title='implement feature BBB', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
    db_session.add(WorkItem(pid=3, title='implement feature CCC', column=3, description='xxxxxxxxxxxxxxxxxxxx'))
    db_session.add(WorkItem(pid=12, title='implement feature XXX', column=1, description='xxxxxxxxxxxxxxxxxxxx'))
    db_session.commit()

`A working example is present in fixtup repository <https://github.com/FabienArcellier/fixtup/tree/master/examples/kanban_flask_sqlite>`__.

.. note::

    In case we need to clean up the database at the end of the test, the ``hook_teardown_data`` hook allows us to do so.

.. note::

    more about :term:`fixture hook`

Mount a fixture in place
************************

To use 2 complementary fixtures, one that mount a database in a docker container and one taht mount a dataset, only the fixture that mount the dataset has to override the working directory. For the fixture that mount
the database, it has to be mounted straight in the template directory.

The flag ``mount_in_place`` in `fixtup.yml` mount the fixture straight in the template directory.

.. code-block:: yaml
    :caption: tests/fixtures/database/fixtup.yml

    keep_mounted: true
    keep_running: true
    mount_in_place: false

.. code-block:: python
    :caption: ./tests/integrations/test_utils.py

    import unittest
    import os

    import fixtup

    class UtilsTest(unittest.TestCase)

        def test_thumbnail_should_generate_thumbnail(self):
            with fixtup.up(['database', 'dataset1']):
                # Given
                wd = os.getcwd()

                # ...


Use Fixtup with other test frameworks
*************************************

``Fixtup`` is agnostic to the testing framework. You should be able to use it with
other frameworks like `robotframework <https://robotframework.org/>`__, ...

Keep a fixture after the end of the test runner for debug purpose
*****************************************************************

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

Mount a fixture once and keep it mounted for all the tests
**********************************************************

When the `keep_mounted` policy is active on a fixture, it is mounted only once at the first test that use this fixture, then reused by each test. Between each test the fixture is starting and stopping. For exemple, with the docker plugin, network is mounted only once. Containers start and stop between every tests.

.. warning:: If you persist information in your test, like create a file or add record in a database, they will be present when fixtup will be running the next test that use this fixture.

When the test runtime stop or when the user interrupts the tests, the fixture is unmounted.

To enable the `keep_mounted` policy, edit `fixtup.yml` in a fixture template

.. code-block:: yaml
    :caption: tests/fixtures/fixtup/simple_fixture/fixtup.yml

    keep_mounted: true
