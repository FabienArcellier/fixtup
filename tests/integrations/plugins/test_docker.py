import os
import unittest

import plumbum

from fixtup import fixtup
from fixtup.entity.fixture import Fixture
from fixtup.plugins.docker import on_mounting, on_starting, on_stopping, on_unmounting
from fixtup.tests.settings import override_fixtup_settings


class TestDocker(unittest.TestCase):

    def test_on_mounting_the_container_and_do_not_start_it(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_docker'):
                # Arrange
                path = os.getcwd()
                fixture_fake = Fixture.fake(identifier='simple_fixture_docker', directory=path)

                # Acts
                try:
                    on_mounting(fixture_fake)

                    # Assert
                    output:str = plumbum.local['docker-compose']('ps')
                    lines = output.split('\n')
                    self.assertEqual(4, len(lines))
                    self.assertIn('sandbox_1', lines[2])
                    self.assertIn('Exit 0', lines[2])
                finally:
                    plumbum.local['docker-compose']('down')

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
                on_mounting(fixture_fake)
                on_starting(fixture_fake)
                on_stopping(fixture_fake)
                on_unmounting(fixture_fake)

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
                on_mounting(fixture_fake)

                try:
                    # Acts
                    on_starting(fixture_fake)

                    # Assert
                    output: str = plumbum.local['docker-compose']('ps')
                    lines = output.split('\n')
                    self.assertEqual(4, len(lines))
                    self.assertIn('sandbox_1', lines[2])
                    self.assertIn('Up', lines[2])
                finally:
                    plumbum.local['docker-compose']('down')

    def test_on_stopping_should_stop_busybox_container(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_docker'):
                # Arrange
                path = os.getcwd()
                fixture_fake = Fixture.fake(identifier='simple_fixture', directory=path)
                on_mounting(fixture_fake)

                try:
                    on_starting(fixture_fake)
                    # Acts

                    on_stopping(fixture_fake)

                    # Assert
                    output: str = plumbum.local['docker-compose']('ps')
                    lines = output.split('\n')
                    self.assertEqual(4, len(lines))
                    self.assertIn('sandbox_1', lines[2])
                    self.assertIn('Exit', lines[2])
                finally:
                    plumbum.local['docker-compose']('down')

    def test_on_unmounting_should_remove_every_trace_of_busybox(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../../fixtures/fixtup"),
            'plugins': []
        }):
            with fixtup.up('simple_fixture_docker'):
                # Arrange
                path = os.getcwd()
                fixture_fake = Fixture.fake(identifier='simple_fixture', directory=path)
                on_mounting(fixture_fake)

                try:
                    on_starting(fixture_fake)
                    on_stopping(fixture_fake)

                    # Acts
                    on_unmounting(fixture_fake)

                    # Assert
                    output: str = plumbum.local['docker-compose']('ps')
                    lines = output.split('\n')
                    self.assertEqual(3, len(lines))
                finally:
                    plumbum.local['docker-compose']('down')


if __name__ == '__main__':
    unittest.main()
