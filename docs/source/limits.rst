Limits
######

Running in CI
=============

If you are specifying external services through docker, your CI platform should support docker service.
We run test for ``Fixtup`` on 2 platforms ``Github Actions`` and ``Gitlab CI``.

Execute test in parallel
========================

If you rely on docker-compose environment or if you use a fixture shared between many tests, you
may not be able to run those tests in parallel.
