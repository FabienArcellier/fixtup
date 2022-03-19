import unittest

import fixtup
from fixtup.fixture.base import fixture_template


class TestFixture(unittest.TestCase):

    def setUp(self):
        pass

    def test_a_fixture_without_manifest_is_not_shared(self):
        with fixtup.up('manifests'):
            # Arrange
            # Acts
            result = fixture_template("my_fixture_1")
            # Assert
            self.assertFalse(result.shared)

    def test_a_fixture_with_manifest_should_read_shared_flag(self):
        with fixtup.up('manifests'):
            # Arrange
            # Acts
            result = fixture_template("my_fixture_2")
            # Assert
            self.assertTrue(result.shared)


if __name__ == '__main__':
    unittest.main()
