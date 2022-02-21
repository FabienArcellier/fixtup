import unittest

from click.testing import CliRunner

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


if __name__ == '__main__':
    unittest.main()
