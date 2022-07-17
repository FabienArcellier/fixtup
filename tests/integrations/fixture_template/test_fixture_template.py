import unittest

from fixtup import fixtup
from fixtup.fixture_template.base import fixture_template


class TestFixtureTemplate(unittest.TestCase):

    def setUp(self):
        pass

    def test_a_fixture_without_manifest_is_not_keep_up(self):
        result = fixture_template("simple_fixture")
        self.assertFalse(result.keep_up)

    def test_a_fixture_with_manifest_should_read_keep_up_flag(self):
        result = fixture_template("simple_fixture_keep_up")
        self.assertTrue(result.keep_up)
