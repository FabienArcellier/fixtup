from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate


def on_new_fixture(template: FixtureTemplate):
    print("on_new_fixture")


def on_mounting(fixture: Fixture):
    print("on_mounting")


def on_starting(fixture: Fixture):
    print("on_starting")


def on_stopping(fixture: Fixture):
    print("on_stopping")


def on_unmounting(fixture: Fixture):
    print("on_unmounting")
