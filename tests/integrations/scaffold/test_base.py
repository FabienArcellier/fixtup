import io
import os
import unittest

import yaml

import fixtup
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.scaffold.base import scaffold_new_fixture
from fixtures import fixture_ctx


class TestScaffold(unittest.TestCase):

    def setUp(self):
        self.context = fixture_ctx.setup_fake()
        self.context.enable_plugins = False

    def tearDown(self) -> None:
        fixture_ctx.teardown_fake()

    def test_scaffold_new_fixture_should_generate_a_fixture_directory(self):
        # Arrange
        with fixtup.up('fixtup_project'):

            fixture_repository = os.path.join(os.getcwd(), "fixtup")
            fixture = FixtureTemplate.fake(identifier='hello world', directory=fixture_repository)

            # Acts
            scaffold_new_fixture(fixture)

            # Assert
            fixture_path = os.path.join(fixture_repository, "hello world")
            self.assertTrue(os.path.isdir(fixture_path), f"fixture does not exists {fixture_path}")

    def test_scaffold_new_fixture_generate_a_valid_yaml_manifest(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), "fixtup")
            fixture = FixtureTemplate.fake(directory=fixture_repository, keep_up=True)

            # Acts
            scaffold_new_fixture(fixture)

            fixtup_manifest = os.path.join(fixture.directory, 'fixtup.yml')
            self.assertTrue(os.path.isfile(fixtup_manifest))

            with io.open(fixtup_manifest) as file_pointer:
                manifest = yaml.load(file_pointer, yaml.SafeLoader)
                self.assertTrue(manifest["keep_up"], f"invalid manifest {manifest}")

    def test_scaffold_new_fixture_generate_a_manifest_with_keep_mounted_policy(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), "fixtup")
            fixture = FixtureTemplate.fake(directory=fixture_repository, keep_mounted=True)

            # Acts
            scaffold_new_fixture(fixture)

            fixtup_manifest = os.path.join(fixture.directory, 'fixtup.yml')
            self.assertTrue(os.path.isfile(fixtup_manifest))

            with io.open(fixtup_manifest) as file_pointer:
                manifest = yaml.load(file_pointer, yaml.SafeLoader)
                template = FixtureTemplate.create_from_fixture_template(fixture.directory, manifest)
                self.assertFalse(template.keep_up)

    def test_scaffold_new_fixture_generate_a_manifest_with_keep_up_policy(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), "fixtup")
            fixture = FixtureTemplate.fake(directory=fixture_repository, keep_up=True)

            # Acts
            scaffold_new_fixture(fixture)

            fixtup_manifest = os.path.join(fixture.directory, 'fixtup.yml')
            self.assertTrue(os.path.isfile(fixtup_manifest))

            with io.open(fixtup_manifest) as file_pointer:
                manifest = yaml.load(file_pointer, yaml.SafeLoader)
                template = FixtureTemplate.create_from_fixture_template(fixture.directory, manifest)
                self.assertTrue(template.keep_up)


if __name__ == '__main__':
    unittest.main()
