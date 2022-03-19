import io
import os
import unittest

import yaml

import fixtup
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.factory import reset_runtime_context, RuntimeContext
from fixtup.scaffold.base import scaffold_new_fixture


class TestScaffold(unittest.TestCase):
    def setUp(self):
        reset_runtime_context(RuntimeContext(unittest=True))

    def test_scaffold_new_fixture_should_generate_a_fixture_directory(self):
        # Arrange
        with fixtup.up('fixtup_project'):

            fixture_repository = os.path.join(os.getcwd(), "fixtup")
            fixture = FixtureTemplate.create_from_cli("hello world", fixture_repository, shared=True)

            # Acts
            scaffold_new_fixture(fixture)

            # Assert
            fixture_path = os.path.join(fixture_repository, "hello world")
            self.assertTrue(os.path.isdir(fixture_path), f"fixture does not exists {fixture_path}")

    def test_scaffold_new_fixture_generate_a_valid_yaml_manifest(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), "fixtup")
            fixture = FixtureTemplate.create_from_cli("hello world", fixture_repository, shared=True)

            # Acts
            scaffold_new_fixture(fixture)

            fixtup_manifest = os.path.join(fixture.directory, 'fixtup.yml')
            self.assertTrue(os.path.isfile(fixtup_manifest))

            with io.open(fixtup_manifest) as file_pointer:
                manifest = yaml.load(file_pointer, yaml.SafeLoader)
                self.assertTrue(manifest["shared"], f"invalid manifest {manifest}")


if __name__ == '__main__':
    unittest.main()
