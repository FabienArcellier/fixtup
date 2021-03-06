.. _plugin:

Plugin
######

The plug-ins in ``Fixtup`` allow you to tune the process of building an environment.
A plug-in runs when a fixture is created, mounted, started, stopped or unmounted.

For example, the ``fixtup.plugins.dotenv`` plugin loads environment variables from an .env file
when starting a fixture. It offers to create the ``.env`` file when generating a new fixture with
the ``fixtup new`` command.

Here are some use cases that could be implemented with a plug-in:

* mount and destroy resources in the cloud with ``terraform`` from a ``terraform.ts`` file
* instantiate resources on a kubernetes cluster during a test
* check the contents of a fixture
* ...

Configure plugins in Fixtup
***************************

A plug-in has to be registers in fixtup settings. If for you it is in a ``setup.cfg`` file, the list of plugins is declared in ``plugins`` section:

.. code-block:: ini
    :caption: ./setup.cfg

    [fixtup]
    fixtures=tests/fixtures
    plugins=
        fixtup.plugins.dotenv
        fixtup.plugins.docker


More information on the configuration in the section :ref:`ConfigureFixtup`

.. note::

    Plugins are executed in their declared order.

    .. figure:: _static/execution_order.png

Native plug-ins
***************

.. toctree::
   :glob:
   :hidden:

   plugins/*

Fixtup implements several plug-ins. They are installed when you install ``fixtup``.

* :ref:`fixtup.plugins.docker <plugins_docker>`: run containers declared in `docker-compose.yml`
* :ref:`fixtup.plugins.dotenv <plugins_dotenv>`: load environment variables for a fixture from a ``.env`` file

Community plugins
*****************

You have created a plugin, you want to share it with the community?
`Contact me on github with this form so it appears here <https://github.com/FabienArcellier/fixtup/issues/new?assignees=&template=new_plugin.md&title=>`__.

Implement your own plug-in
**************************

To implement a plug-in, you need to implement a module with those functions.
The functions are optional, if they are absent, ``fixtup`` will not take them into account.

.. code-block:: python
    :caption: src/fixtup_terraform/plugin.py

    import io
    import os

    from fixtup.prompt.factory import lookup_prompt
    from fixtup.entity.fixture import Fixture
    from fixtup.entity.fixture_template import FixtureTemplate


    def on_new_fixture(template: FixtureTemplate):
        """
        This function is called by fixtup when a developer instantiates a new fixture with ``fixtup new``.
        It's the place to bootstrap content relative to your plugin.

        For example, the plugin can create a terraform.tf file if the developer plans to use terraform.
        """
        prompt = lookup_prompt()
        is_terraform = prompt.confirm('Is this fixture use terraform declaration ?')
        if is_terraform:
            with io.open(os.path.join(template.directory, 'terraform.tf'), 'w') as fp:
                pass

    def on_setup_data(fixture: Fixture):
        """
        This function is called by fixtup between each test to provision data
        """
        pass

    def on_starting(fixture: Fixture):
        """
        this function is called by fixtup every time it need to start a test that requires the fixture.
        """
        pass

    def on_stopping(fixture: Fixture):
        """
        this function is called by fixtup every time it end a test.
        """
        pass

    def on_teardown_data(fixture: Fixture):
        """
        This function is called by fixtup between each test to cleanup data
        """
        pass


In the configuration file, you must add the module of your plugin.

.. code-block:: ini
    :caption: ./setup.cfg

    [fixtup]
    fixtures=tests/fixtures
    plugins=
        fixtup.plugins.dotenv
        fixtup.plugins.docker
        fixtup_terraform.plugin
