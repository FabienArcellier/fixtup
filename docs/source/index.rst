Fixtup
######

.. figure:: _static/principle_simplified_diagram.png
    :align: center

Do you have already given up on writing integration tests ?

* it would have been too complicated to mount several containers to run these tests
* it would have been necessary to write too much boilerplate to run these tests in a CI
* it would have taken another developer too many steps to run these tests
* it would have been difficult to debug them individually in an IDE

With Fixtup, **write clear, robust and easy-to-execute integration tests** with your favorite test framwork like ``pytest``, ``unittest`` or event BDD framework as ``robot framework`` or ``behave``.

* it starts the services needed to run your test
* it throws the longest fixtures only once whether you play a test or 100
* it cleans files and data between each test
* it runs on a developer's workstation without configuration

Benefits
********

* You can get up and running with Fixtup **in minutes**, even on legacy project, **no matter what your test framework is**.
* You will **stop wasting your time on boilerplate code**
* Fixtup provides an easy way to **run tests in debug in your favorite IDE like pycharm and vscode**.
* Fixtup is cross-platform which makes it easy to use it on Linux, Mac and Windows.

.. toctree::
    :maxdepth: 2
    :caption: Table of content

    getting_started
    install
    handbook
    plugin
    limits
    concepts
    support
    command_line
    api

Indices and tables
==================

* :ref:`search`
