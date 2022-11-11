import os
import unittest

from fixtup.entity.settings import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.fake_manifest_dir = 'hello/world'
        pass

    def test_configuration_dir_should_return_the_directory_of_the_manifest(self):
        # Arrange
        settings = Settings.from_manifest("hello/world/setup.cfg", {'fixtures': "test/fixtures"})

        # Acts & Assert
        expected_path = os.path.join("hello", "world")
        self.assertIn(expected_path, settings.configuration_dir)

    def test_from_manifest_should_extract_fixture(self):
        # Arrange

        # Acts
        entity = Settings.from_manifest(self.fake_manifest_dir, {"fixtures": "test/fixtures"})

        # Assert
        expected_path = os.path.join("test", "fixtures")
        self.assertEqual(expected_path, entity.fixtures)

    def test_from_manifest_should_extract_plugins_list(self):
        # Arrange

        # Acts
        entity = Settings.from_manifest(self.fake_manifest_dir, {
            "fixtures": "test/fixtures",
            "plugins": [
                "fixtup.plugins.docker"
            ]
        })

        # Assert
        self.assertEqual(["fixtup.plugins.docker"], entity.plugins)

    def test_from_manifest_should_ignore_attributes_that_does_not_exists_in_settings(self):
        # Arrange

        # Acts
        entity = Settings.from_manifest(
            self.fake_manifest_dir,
            {
                "fixtures": "test/fixtures",
                "stupid_attribute": []
            }
        )

        # Assert
        self.assertFalse(hasattr(entity, "stupid_attribute"))

    def test_from_manifest_should_ignore_missing_plugins_attribute(self):
        # Arrange

        # Acts
        entity = Settings.from_manifest(self.fake_manifest_dir, {"fixtures": "test/fixtures"})

        # Assert
        self.assertEqual([], entity.plugins)


if __name__ == '__main__':
    unittest.main()
