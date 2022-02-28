import io
import os
import unittest

from click.testing import CliRunner

import fixtup
from fixtup.cli.base import cli
from fixtup.factory import RuntimeContext, reset_runtime_context
from fixtup.prompt.mock import send_text, reset_input
from fixtup.settings import read_settings


class TestCli(unittest.TestCase):
    def setUp(self):
        reset_input()
        reset_runtime_context(RuntimeContext(unittest=True))
        self._runner = CliRunner()

    def test_invoke_should_show_a_list_of_command(self):
        # Arrange
        # Acts
        result = self._runner.invoke(cli)
        # Assert
        self.assertIn("  new", result.output)
        self.assertIn("  init", result.output)

    def test_info_should_show_error_when_fixtup_is_not_configured(self):
        # Arrange
        with fixtup.up('python_project'):
            # Acts
            result = self._runner.invoke(cli, ['info'])
            # Assert
            self.assertIn("fixtup not configured in this project", result.output)

    def test_info_should_show_information_when_fixtup_is_configured(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            # Acts
            result = self._runner.invoke(cli, ['info'])
            # Assert
            self.assertIn("Configuration", result.output)
            self.assertIn("Fixtures", result.output)

    def test_new_should_generate_a_new_fixture(self):
        # Arrange
        send_text("hello world")
        send_text("y")

        with fixtup.up('fixtup_project'):
            # Acts
            settings = read_settings()

            result = self._runner.invoke(cli, ['new'])

            # Assert
            fixture_path = os.path.join(settings.fixtures_dir, "hello world")
            self.assertTrue(os.path.isdir(fixture_path), f"fixture does not exists {fixture_path}")

            fixtup_manifest = os.path.join(fixture_path, 'fixtup.yml')
            self.assertTrue(os.path.isfile(fixtup_manifest))

if __name__ == '__main__':
    unittest.main()
