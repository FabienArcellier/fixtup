import os
import unittest

import fixtup
from fixtup.settings.pyproject_toml import PyprojectToml


class TestPyprojectToml(unittest.TestCase):
    def setUp(self):
        self._tested = PyprojectToml()

    def test_has_manifest_should_check_the_manifest_exists(self):
        # Arrange
        with fixtup.up('manifests'):
            cwd = os.getcwd()

            # Acts
            manifest_is_present = self._tested.has_manifest(cwd)

            # Assert
            self.assertTrue(manifest_is_present)

    def test_has_manifest_should_check_the_manifest_is_missing(self):
        # Arrange
        with fixtup.up('manifests_missing'):
            cwd = os.getcwd()

            # Acts
            manifest_is_present = self._tested.has_manifest(cwd)

            # Assert
            self.assertFalse(manifest_is_present)

    def test_contains_settings_should_check_if_fixtup_section_is_present_in_manifest(self):
        # Arrange
        with fixtup.up('manifests'):
            cwd = os.getcwd()

            # Acts
            section_is_present = self._tested.contains_settings(cwd)
            # Assert
            self.assertTrue(section_is_present)

    def test_contains_settings_should_check_if_fixtup_section_is_missing_in_manifest(self):
        # Arrange
        with fixtup.up('manifests_empty') as wd:
            cwd = os.getcwd()

            # Acts
            section_is_present = self._tested.contains_settings(cwd)
            # Assert
            self.assertFalse(section_is_present)

    def test_read_settings_should_load_manifest_information(self):
        # Arrange
        with fixtup.up('manifests') as wd:
            cwd = os.getcwd()

            # Acts
            settings = self._tested.read_settings(cwd)

            # Assert
            expected_path = os.path.join("tests", "fixtures", "fixtup")
            self.assertEqual(expected_path, settings.fixtures)
            self.assertIn("fixtup.plugins.docker", settings.plugins)


if __name__ == '__main__':
    unittest.main()
