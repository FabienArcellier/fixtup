import os
import unittest

import fixtup
from fixtup.entity.fixture import Fixture
from fixtup.plugins import dotenv
from fixtup.tests.settings import override_fixtup_settings
from fixtures import fixture_context


class TestDotenv(unittest.TestCase):

    def setUp(self) -> None:
        self.context = fixture_context.setup_fake()
        self.context.enable_plugins = True
        self.context.emulate_new_process = True

    def tearDown(self) -> None:
        fixture_context.teardown_fake()

    def test_on_starting_should_override_environments_variables(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_dotenv'):
                # Arrange
                fixture = Fixture.fake(directory=os.getcwd())
                self.assertIsNone(os.getenv('FIXTUP_HELLO'))

                # Acts
                try:
                    dotenv.on_starting(fixture)

                    # Assert
                    self.assertEqual('world', os.getenv('FIXTUP_HELLO'))
                finally:
                    dotenv.on_stopping(fixture)

    def test_on_stopping_should_restore_environments_variables(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_dotenv'):
                # Arrange
                fixture = Fixture.fake(directory=os.getcwd())
                dotenv.on_starting(fixture)
                self.assertEqual('world', os.getenv('FIXTUP_HELLO'))

                # Acts
                dotenv.on_stopping(fixture)

                # Assert
                self.assertIsNone(os.getenv('FIXTUP_HELLO'))

    def test_on_stopping_should_restore_environments_variables_modified_after_starting(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_dotenv'):
                # Arrange
                fixture = Fixture.fake(directory=os.getcwd())
                dotenv.on_starting(fixture)
                os.environ['HELLO'] = 'test'

                # Acts
                dotenv.on_stopping(fixture)

                # Assert
                self.assertIsNone(os.getenv('FIXTUP_HELLO'))
                self.assertIsNone(os.getenv('HELLO'))


if __name__ == '__main__':
    unittest.main()
