import sys

import os
import unittest

import plumbum

from fixtup import fixtup
from fixtup.entity.fixture import Fixture
from fixtup.plugins.docker import on_starting, on_stopping
from fixtup.tests.settings import override_fixtup_settings


class TestDocker(unittest.TestCase):

    def test_docker_plugin_should_do_nothing_when_there_is_no_docker_compose_file(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture'):
                # Arrange
                path = os.getcwd()
                fixture_fake = Fixture.fake(identifier='simple_fixture', directory=path)

                # Acts
                on_starting(fixture_fake)
                on_stopping(fixture_fake)

                # Assert
                # This is a smoke test. If docker-compose is invoked, it will raise an exception.
                # We check the fixture directory does not have a docker-compose.yml file.
                self.assertFalse(os.path.isfile(os.path.join(path, 'docker-compose.yml')))

    def test_on_starting_should_start_busybox_container(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_docker'):
                # Arrange
                path = os.getcwd()
                fixture_fake = Fixture.fake(identifier='simple_fixture', directory=path)

                try:
                    # Acts
                    on_starting(fixture_fake)

                    # Assert
                    output: str = plumbum.local['docker-compose']('ps')
                    output_row = output.split(os.sep)

                    splitted_path = os.path.split(path)
                    docker_compose_prefix = splitted_path[-1]

                    docker_compose_identifier = _docker_compose_identifier(docker_compose_prefix, 'sandbox', 1)
                    self.assertIn(docker_compose_identifier, output_row[-1])

                    if _if_linux():
                        self.assertIn(f'Up', output_row[-1])

                    if _if_macos():
                        self.assertIn(f'running', output_row[-1])
                finally:
                    plumbum.local['docker-compose']('down')

    def test_on_stopping_should_stop_and_remove_every_trace_of_busybox(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_docker'):
                # Arrange
                path = os.getcwd()
                fixture_fake = Fixture.fake(identifier='simple_fixture', directory=path)

                try:
                    on_starting(fixture_fake)

                    # Acts
                    on_stopping(fixture_fake)

                    # Assert
                    output: str = plumbum.local['docker-compose']('ps')
                    output_row = output.split(os.sep)

                    splitted_path = os.path.split(path)
                    docker_compose_prefix = splitted_path[-1]
                    docker_compose_identifier = _docker_compose_identifier(docker_compose_prefix, 'sandbox', 1)
                    self.assertNotIn(docker_compose_identifier, output_row[-1])
                finally:
                    plumbum.local['docker-compose']('down')


def _docker_compose_identifier(docker_prefix: str, identifier: str, index: int) -> str:
    """
    Docker compose build different identifier that depends of the platform

    on linux, _ is used as separator
    on macos, - is used as separator

    linux : simple_fixture_docker__l16555o3_sandbox_1
    macos : simple_fixture_docker__l16555o3-sandbox-1
    """
    if _if_linux():  # could be "linux", "linux2", "linux3", ...
        return f"{docker_prefix}_{identifier}_{index}"

    if _if_macos():
        return f"{docker_prefix}-{identifier}-{index}"

    raise OSError(f"not supported platform : {sys.platform}")


def _if_linux() -> bool:
    return sys.platform.startswith("linux")


def _if_macos() -> bool:
    return sys.platform == "darwin"


if __name__ == '__main__':
    unittest.main()
