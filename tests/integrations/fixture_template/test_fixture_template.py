import os

import unittest

from fixtup import fixtup
from fixtup.fixture_template.base import fixture_template
from fixtures import fixture_ctx


class TestFixtureTemplate(unittest.TestCase):

    def setUp(self) -> None:
        self.context = fixture_ctx.setup_fake()
        self.context.emulate_new_process = True
        self.context.fixturesdir = os.path.realpath(os.path.join(__file__, '..', '..', '..', 'fixtures', 'fixtup'))

    def tearDown(self):
        fixture_ctx.teardown_fake()

    def test_a_fixture_without_manifest_is_not_keep_up(self):
        result = fixture_template("simple_fixture")
        self.assertFalse(result.keep_up)

    def test_a_fixture_with_manifest_should_read_keep_up_flag(self):
        result = fixture_template("simple_fixture_keep_up")
        self.assertTrue(result.keep_up)
