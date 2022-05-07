.. _plugins_dotenv:

fixtup.plugins.dotenv
#####################

It loads environment variables from a `.env` file. At the end of the test, the environment variables
are restored to their original values.

.. warning::

    Variables that have been modified or added during the test will also be restored to their original value
    or erased.

    .. code-block:: python

        with fixtup.up('simple'):
            os.environ['HELLO'] = 'hello'
            # dispaly hello
            print(os.getenv('HELLO'))

        # display None
        print(os.getenv('HELLO'))


Configuration
*************

.. code-block::
    :caption: ./setup.cfg

    [fixtup]
    plugins=
        fixtup.plugins.dotenv

Common options
**************


