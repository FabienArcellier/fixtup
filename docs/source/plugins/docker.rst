fixtup.plugins.docker
#####################

It run containers declared in the fixture by ``docker-compose.yml``. If containers are missing, they are downloaded at the first
execution. The container run in the directory the fixture has been created. So when a fixture is mounted, containers are
created from scratch. You can't use volume to share state.

The infrastructure describe in ``docker-compose.yml`` is built when a fixture is mounted. The containers will start
just after when the fixture start. They will be running till the fixture is stopped. All traces of containers and networks
are clean-up when the fixture is unmounted.

Usage
*****

.. code-block::
    :caption: ./setup.cfg

    [fixtup]
    plugins=
        fixtup.plugins.docker

Common options
**************

You can tune the behavior of ``fixtup.plugins.docker`` plugin through environment variables.

* ``FIXTUP_DOCKER_VERBOSE`` : It will show in terminal the logs from containers when a fixture is ``stopped``

    * value : any value will trigger the behavior
