import unittest

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate


class TestFixture(unittest.TestCase):

    def test_create_from_template_should_extract_fixture_identifier_from_the_path(self):
        # Arrange
        fixture_template = FixtureTemplate.fake()

        # Acts
        fixture = Fixture.create_from_template(fixture_template, '/tmp/simple_database_tr45er8')
        # Assert
        self.assertEqual('simple_database_tr45er8', fixture.identifier)


if __name__ == '__main__':
    unittest.main()
