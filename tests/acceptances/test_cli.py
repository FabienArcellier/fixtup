import unittest

from click.testing import CliRunner

import fixtup
from fixtup.cli.base import cli


class TestCli(unittest.TestCase):
    def setUp(self):
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

if __name__ == '__main__':
    unittest.main()
