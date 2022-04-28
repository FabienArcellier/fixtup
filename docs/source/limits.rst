Limits
######

Running docker in CI
====================

If you are specifying external services through docker, your CI platform should support docker service.
We run test for ``Fixtup`` on 2 platforms ``Github Actions`` and ``Gitlab CI``.

Running tests in parallel
=========================

Fixtup doesn't work well when your tests are run in parallel with ``pytest-xdist`` for example.

Features will give you trouble because fixtup does not manage locks to wait for the test that uses
the fixture has finished executing.

Here are some examples :

* If a fixture instantiates a container on a port with docker-compose, docker will refuse to start a second fixture
* If a fixture remains up with a ``keep_mounted`` policy between 2 tests played in parallel, you risk data consistency
  issue in the fixture directory
* ...
