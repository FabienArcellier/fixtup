import os.path

import unittest

import fixtup
from fixtup.exceptions import PythonManifestMissing
from fixtup.settings.base import list_project_manifests, read_settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        pass

    def test_list_project_manifests_should_return_both_manifests_if_both_are_present(self):
        # Arrange
        with fixtup.up('manifests'):
            # Acts
            _available_manifests = list_project_manifests()

            # Assert
            self.assertEqual(['setup.cfg', 'pyproject.toml'], _available_manifests.prompt_choices())

    def test_list_project_manifests_should_raise_exception_if_no_manifest_exists(self):
        # Arrange
        with fixtup.up('manifests_missing'):
            # Acts
            try:
                _available_manifests = list_project_manifests()
                self.fail('python manifest is missing, this test should raise an exception')
            # Assert
            except PythonManifestMissing as exception:
                pass

    def test_read_settings_should_create_fixture_directory_when_missing(self):
        # Arrange
        with fixtup.up('fixtup_project_missing_fixtup_directory'):
            # Acts
            settings = read_settings()
            # Assert
            self.assertTrue(os.path.isdir(settings.fixtures_dir), f"{settings.fixtures_dir} must exist")


if __name__ == '__main__':
    unittest.main()
