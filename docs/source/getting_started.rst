Getting Started
###############

Let's discover in 10 minutes how fixtup will simplify the writing of your integration tests.

In this tutorial, we are going to write 2 tests that validate a miniature manufacturing utility.
Fixtup will help us build an environment that contains 2 images to miniaturize.

.. contents::
    :backlinks: top
    :local:

Clone the getting started project
*********************************

.. code-block:: bash

    git clone https://github.com/FabienArcellier/fixtup-getting-started.git
    cd fixtup-getting-started
    pip install .

pip install the library Pillow used to miniaturize images.

Install and configure fixtup
****************************

.. code-block:: bash

    pip install fixtup

The first thing to do is to configure `fixtup`. the cli is here to make your life easier.
With the ``fixtup init`` command.

.. code-block:: bash

    $ fixtup init
    Fixtures repository ? tests/fixtures
    Python manifest ? setup.cfg

.. note::

    more about :ref:`CommandLine`

In the next step you need to configure `Fixtup` in your project manifest
``setup.cfg``. You will declare a directory that will contains your fixtures.

.. code-block:: ini
    :caption: ./setup.cfg

    [fixtup]
    fixtures=tests/fixtures
    plugins=
        fixtup.plugins.dotenv
        fixtup.plugins.docker

Scaffold your first fixture
***************************

.. code-block:: bash

    $ fixture new
    Fixture identifier ? thumbnail_context
    Is this fixture is shared between all the tests ? no

This command scaffold a new :term:`fixture template`. It is generated in ``tests/fixtures/thumbnail_context``.

You will add those 3 files inside this directory:

* `img1.png <_static/img1.png>`__
* `img2.png <_static/img2.png>`__
* `img3.png <_static/img3.png>`__

.. code-block:: bash

    cd tests/fixtures/thumbnail_context
    wget https://fixtup.readthedocs.io/en/latest/_static/img1.png
    wget https://fixtup.readthedocs.io/en/latest/_static/img2.png
    wget https://fixtup.readthedocs.io/en/latest/_static/img3.png

.. note::

    A fixture template contains several files that depend on which plugins are active. By default there is
    a manifest `fixtup.yml` and a folder `.hooks` that contains the different :term:`fixture hook`
    you can use to load data, download files, ...

Test with unittest
==================

It's time to test the function ``thumbnail`` with ``unittest``. We will call our fixture in the test with ``fixtup.up``.

.. code-block:: python
    :caption: ./tests/integrations/test_utils.py

    import unittest
    import os

    import fixtup

    class UtilsTest(unittest.TestCase)

        def test_thumbnail_should_generate_thumbnail(self):
            with fixtup.up('thumbnail_context'):
                # Given
                wd = os.getcwd()

                original_file = os.path.join(wd, 'img1.png')
                expected_thumbnail_file = os.path.join(wd, 'img1_t.png')

                # When
                thumbnail(original_file, expected_thumbnail_file)

                # Then
                self.assertTrue(os.path.isfile(expected_thumbnail_file)

On every test invocation, ``Fixtup`` will create a working directory in your ``/tmp``. This directory is a clone of
the one defined in ``tests/fixtures/thumbnail_context``.

.. note::

    On your computer, it may be different. ``Fixtup`` use temporary directory of the system.
    `/tmp` is usually the one on linux based environment.

When the context is closing, this directory is destroyed. If you want to check what happen inside, you have to
stop the code execution with a breakpoint on the assertion line and check what is inside.

Test with pytest
================

``Fixtup`` works the same with ``pytest``. We will call our fixture in the test with ``fixtup.up``.

.. code-block:: python
    :caption: ./tests/integrations/test_utils.py

    import fixtup

    def test_thumbnail_should_generate_thumbnail():
        with fixtup.up('thumbnail_context'):
            # Given
            wd = os.getcwd()

            original_file = os.path.join(wd, 'img1.png')
            expected_thumbnail_file = os.path.join(wd, 'img1_t.png')

            # When
            thumbnail(original_file, expected_thumbnail_file)

            # Then
            self.assertTrue(os.path.isfile(expected_thumbnail_file)


On every test invocation, ``Fixtup`` will create a working directory in your ``/tmp``. This directory is a clone of
the one defined in ``tests/fixtures/thumbnail_context``.

When the context is closing, this directory is destroyed. If you want to check what happen inside, you have to
stop the code execution with a breakpoint on the assertion line and check what is inside.

Use in a pytest fixture
-----------------------

To write once the initialization code of a fixture of ``Fixtup`` and use it in many tests, you can write a fixture for
``pytest``.

.. code-block:: python
    :caption: ./tests/integrations/test_utils.py

    def thumbnail_context():
        with fixtup.up('thumbnail_context'):
            yield None


    def test_thumbnail_should_generate_thumbnail(thumbnail_context):
        # Given
        wd = os.getcwd()

        original_file = os.path.join(wd, 'img1.png')
        expected_thumbnail_file = os.path.join(wd, 'img1_t.png')

        # When
        thumbnail(original_file, expected_thumbnail_file)

        # Then
        self.assertTrue(os.path.isfile(expected_thumbnail_file)



Start with other stacks
***********************

In `fixtup repository <https://github.com/FabienArcellier/fixtup/tree/master/examples>`__, you will find examples on how to implement integration tests with fixtup on other stacks.

* `use fixtup to test a python script that generate thumbnail <https://github.com/FabienArcellier/fixtup/tree/master/examples/unittest>`__
* `use fixtup to manage test environments with sqlite database on flask <https://github.com/FabienArcellier/fixtup/blob/master/examples/kanban_flask_sqlite>`__

Your contributions are welcome to add your stack. More information in `CONTRIBUTING.md <https://github.com/FabienArcellier/fixtup/blob/master/CONTRIBUTING.md#implement-a-new-example-for-your-own-stack>`__
