Concepts
########

``Fixtup`` concepts are described on this page. They can help you
to better understand the advanced features.

.. glossary::

    fixture
        A fixture represent an isolated environment mount from a fixture template. A fixture usually live the time
        of the test. It's behavior can be tune by policies

    fixture hook
        hooks allow you to execute your own code when starting or stopping a fixture. There is a hook
        for each change of state in :term:`fixture livecycle`. A hook is a python module inside
        of a fixture template. They are optional.

        hook usecases :

        * :ref:`HookWaitAvailability`
        * :ref:`HookLoadData`
        * clean-up data from sqlite or postgres database
        * ...

        fixtup propose 6 hooks.

            * ``hook_mounted.py`` : executed when the fixture is mounted, i.e. the fixture's template folder is copied
            * ``hook_started.py`` : executed when the fixture is started and every plugin has been runned, for example after docker-compose has run and after environment variables have been loaded
            * ``hook_setup_data.py`` : runs between each test to mount data required at the start of the test. This hook is executed every time, even if the fixture remains in the ``running`` state between each test.
            * ``hook_stopping.py`` : executed when the fixture stops
            * ``hook_teardown_data.py`` : runs at the end of each test to clean up the data mounted at the ``setup_data`` step.
            * ``hook_unmounting.py`` : executed before the folder containing the fixture is deleted

    fixture livecycle
        A fixture has a livecycle. Unmounted fixture does not have physical existence. When
        a fixture is mounted, a space is created on disk to hold fixture content and environment. When it's started, the  environment relative to the fixture is running. It may be containers, environments variable, ...

        .. figure:: _static/fixture_livecycle.png
            :align: center

    fixture template
        A fixture template is a definition of the environment to mount in a fixture. Fixtup takes the fixture template
        and instanciate a fixture from it.

    plugin
        A plugin adds functionality to fixtup. A plugin is invoked during transitions in the lifecycle.
        The fixtup plugins rely on a definition file present in the fixture template. For example, `.env` for
        `fixtup.plugins.dotenv` plugin or `docker-compose.yml` for `fixtup.plugins.docker`.

        :ref:`more about plugin <plugin>`

