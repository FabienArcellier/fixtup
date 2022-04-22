Fixtup
######

You will love writing integration tests in python with ``Fixtup``.


.. figure:: _static/principle_simplified_diagram.png
    :align: center

Some of your tests need a database, a folder with data, dedicated environment variables,
``Fixtup`` provides all of this for you. Don't even bother to take care of the cleaning,
it releases by itself the resources that it has provisioned.

``Fixtup`` makes it easy to use external dependencies in your tests. It integrates
to your favorite test framework like pytest, unitest or even BDD framework like robot framework
or behave.

.. code-block:: python

    import unittest
    import os
    import fixtup

    class UtilsTest(unittest.TestCase)
        def test_thumbnail_should_generate_thumbnail(self):

            # Magic happens with the instruction fixtup.up
            with fixtup.up('thumbnail_context'):
                # Given
                wd = os.getcwd()
                original_file = os.path.join(wd, 'file.png')
                expected_thumbnail_file = os.path.join(wd, 'file_t.png')

                # When
                thumbnail(original_file, expected_thumbnail_file)

                # Then
                self.assertTrue(os.path.isfile(expected_thumbnail_file)

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
