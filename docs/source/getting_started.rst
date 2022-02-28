Getting Started
###############

.. contents::
    :backlinks: top

On this page, you will start a new project to show how to use ``Fixtup``.
You should have ten minutes to follow this tuorial.

First, you have to install fixtup in your python environment.

.. code-block:: bash

    pip install fixtup

In this example, we will use this organisation for our code repository. We will create those elements
one by one. Vous retrouverez cet exemple complet dans le repository de code de ``Fixtup`` dans
``examples/unittests``.

.. code-block:: text

    .
    ├── lib
    │   ├── __init__.py
    │   └── utils.py
    ├── pyproject.toml
    ├── setup.cfg
    └── tests
        ├── fixtures
        │   └── thumbnail_context
        |       ├── fixtup.yml
        │       └── file.png
        └── integrations
            ├── __init__.py
            └── test_utils.py

In the next step you need to configure `Fixtup` in your project manifest
``setup.cfg``. You will declare a directory that will contains your fixtures.

.. code-block:: ini
    :caption: ./setup.cfg

    [fixtup]
    fixtures=tests/fixtures

Before writing your first fixture, you will implement the function thumbnail in ``lib/utils.py``.
To run the function thumbnail, you need to setup pillow in your python environment ``pip install Pillow``.

.. code-block:: python
    :caption: lib/utils.py

    from PIL import Image

    def thumbnail(image: str, thumbnail: str) -> None:
        resize = (128, 128)
        img = Image.open(image)
        img = img.resize(resize, Image.ANTIALIAS)
        img.save(thumbnail)

This function work on a file, build a new file. To test it, we need a file and a working directory.
``Fixtup`` will give you both.

.. code-block:: bash

    fixture new --key thumbnail_context

Cette commande initialise une nouvelle fixture. Sans option, c'est juste un dossier vide. Il est stocké dans
``tests/fixtures/thumbnail_context``. Nous allons ajouter l'image ``file.png`` dans ce dossier.

.. image:: _static/file.png

Test with unittest
*****************************

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

                original_file = os.path.join(wd, 'file.png')
                expected_thumbnail_file = os.path.join(wd, 'file_t.png')

                # When
                thumbnail(original_file, expected_thumbnail_file)

                # Then
                self.assertTrue(os.path.isfile(expected_thumbnail_file)

On every test invocation, ``Fixtup`` will create a working directory in your ``/tmp``. This directory is a clone of
the one defined in ``tests/fixtures/thumbnail_context``.

When the context is closing, this directory is destroyed. If you want to check what happen inside, you have to
stop the code execution with a breakpoint on the assertion line and check what is inside.

Use in setUp
============

You can use the same fixture for all the tests in one test case using ``setUp``. The fixture will be destroyed at the
end of each test. You don't have to write the code for the ``tearDown``.

.. code-block:: python
    :caption: ./tests/integrations/test_utils.py

    import unittest
    import os

    import fixtup

    class UtilsTest(unittest.TestCase):

        def setUp(self):
            fixtup.use(self, 'thumbnail_context')

        def test_thumbnail_should_generate_thumbnail(self):
            # Given
            wd = os.getcwd()

            original_file = os.path.join(wd, 'file.png')
            expected_thumbnail_file = os.path.join(wd, 'file_t.png')

            # When
            thumbnail(original_file, expected_thumbnail_file)

            # Then
            self.assertTrue(os.path.isfile(expected_thumbnail_file)

Test with pytest
***************************

``Fixtup`` works the same with ``pytest``. We will call our fixture in the test with ``fixtup.up``.

.. code-block:: python
    :caption: ./tests/integrations/test_utils.py

    import fixtup

    def test_thumbnail_should_generate_thumbnail():
        with fixtup.up('thumbnail_context'):
            # Given
            wd = os.getcwd()

            original_file = os.path.join(wd, 'file.png')
            expected_thumbnail_file = os.path.join(wd, 'file_t.png')

            # When
            thumbnail(original_file, expected_thumbnail_file)

            # Then
            self.assertTrue(os.path.isfile(expected_thumbnail_file)


On every test invocation, ``Fixtup`` will create a working directory in your ``/tmp``. This directory is a clone of
the one defined in ``tests/fixtures/thumbnail_context``.

When the context is closing, this directory is destroyed. If you want to check what happen inside, you have to
stop the code execution with a breakpoint on the assertion line and check what is inside.

Use in a pytest fixture
=======================

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

        original_file = os.path.join(wd, 'file.png')
        expected_thumbnail_file = os.path.join(wd, 'file_t.png')

        # When
        thumbnail(original_file, expected_thumbnail_file)

        # Then
        self.assertTrue(os.path.isfile(expected_thumbnail_file)
