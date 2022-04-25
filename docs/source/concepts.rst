Concepts
########

``Fixtup`` concepts are described on this page. They can help you
to better understand the advanced features.

.. glossary::

    fixture
        A fixture represent an isolated environment mount from a fixture template. A fixture usually live the time
        of the test. It's behavior can be tune by policies

    fixture livecycle
        A fixture has a livecycle. Unmounted fixture does not have physical existence. When
        a fixture is mounted, a space is created on disk to hold fixture content and environment. When it's started,
        the  environment relative to the fixture is running. It may be containers, environments variable, ...

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

