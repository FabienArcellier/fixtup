import unittest

from fixtup.entity.settings import Settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.fake_manifest_dir = 'hello/world'
        pass

    def test_from_manifest_should_extract_fixture(self):
        # Arrange

        # Acts
        entity = Settings.from_manifest(self.fake_manifest_dir, {"fixtures": "test/fixtures"})

        # Assert
        self.assertEqual("test/fixtures", entity.fixtures)

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


if __name__ == '__main__':
    unittest.main()
