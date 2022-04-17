import os
import unittest

from click.testing import CliRunner

import fixtup
from fixtup.cli.base import cli
from fixtup.factory import RuntimeContext, reset_runtime_context
from fixtup.prompt.mock import send_text, reset_input
from fixtup.settings import read_settings
from fixtup.tests.settings import override_fixtup_settings


class TestCli(unittest.TestCase):

    def setUp(self):
        reset_input()
        reset_runtime_context(RuntimeContext(unittest=True, enable_plugins=False))
        self._runner = CliRunner()

    def tearDown(self) -> None:
        reset_runtime_context()

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

    def test_init_should_configure_a_project_to_use_fixtup(self):
        # Arrange
        send_text("tests/fixture")
        send_text("setup.cfg")

        with fixtup.up('python_project'):
            # Acts
            result = self._runner.invoke(cli, ['init'])

            # Assert
            self.assertEqual(0, result.exit_code)

            settings = read_settings()
            self.assertEqual("tests/fixture", settings.fixtures)
            self.assertIn("fixtup.plugins.docker", settings.plugins)

    def test_init_should_configure_a_project_with_setup_cfg_valid_with_info(self):
        # Arrange
        send_text("tests/fixture")
        send_text("setup.cfg")

        with fixtup.up('python_project'):
            # Acts
            self._runner.invoke(cli, ['init'])
            result = self._runner.invoke(cli, ['info'])

            # Assert
            self.assertEqual(0, result.exit_code)

    def test_init_should_configure_a_project_with_pyproject_toml_valid_with_info(self):
        # Arrange
        send_text("tests/fixture")
        send_text("pyproject.toml")

        with fixtup.up('python_project'):
            # Acts
            self._runner.invoke(cli, ['init'])
            result = self._runner.invoke(cli, ['info'])

            # Assert
            self.assertEqual(0, result.exit_code, result.output)

    def test_init_should_ignore_a_project_already_configured(self):
        # Arrange
        send_text("tests/fixture")
        send_text("setup.cfg")

        with fixtup.up('fixtup_project'):
            # Acts
            result = self._runner.invoke(cli, ['init'])

            # Assert
            self.assertEqual(2, result.exit_code)
            self.assertIn("Fixtup is already configured, use fixtup info for more info", result.output)

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

    def test_new_should_ask_for_docker_template(self):
        # Arrange
        reset_runtime_context(RuntimeContext(unittest=True, enable_plugins=True))

        send_text("hello world")
        send_text("y")
        send_text("y")

        with fixtup.up('fixtup_project'):
            with override_fixtup_settings({
                "fixtures": os.getcwd(),
                'plugins': [
                    'fixtup.plugins.docker'
                ]
            }):

                # Acts
                settings = read_settings()

                result = self._runner.invoke(cli, ['new'])

                # Assert
                self.assertEqual(0, result.exit_code)

                fixture_path = os.path.join(settings.fixtures_dir, "hello world")
                self.assertTrue(os.path.isdir(fixture_path), f"fixture does not exists {fixture_path}")

                docker_compose_path = os.path.join(fixture_path, 'docker-compose.yml')
                self.assertTrue(os.path.isfile(docker_compose_path))


    def test_new_should_ask_for_docker_template_and_not_create_the_template_when_the_user_refuse(self):
        # Arrange
        reset_runtime_context(RuntimeContext(unittest=True, enable_plugins=True))

        send_text("hello world")
        send_text("y")
        send_text("n")

        with fixtup.up('fixtup_project'):
            with override_fixtup_settings({
                "fixtures": os.getcwd(),
                'plugins': [
                    'fixtup.plugins.docker'
                ]
            }):

                # Acts
                settings = read_settings()

                result = self._runner.invoke(cli, ['new'])

                # Assert
                self.assertEqual(0, result.exit_code)

                fixture_path = os.path.join(settings.fixtures_dir, "hello world")
                self.assertTrue(os.path.isdir(fixture_path), f"fixture does not exists {fixture_path}")

                docker_compose_path = os.path.join(fixture_path, 'docker-compose.yml')
                self.assertFalse(os.path.isfile(docker_compose_path))

if __name__ == '__main__':
    unittest.main()
