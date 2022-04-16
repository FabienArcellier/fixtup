import io
import os

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate


def on_new_fixture(template: FixtureTemplate):
    pass


def on_mounting(fixture: Fixture):
    for i in range(0, 10, 1):
        _call_error()


def on_starting(fixture: Fixture):
    pass


def on_stopping(fixture: Fixture):
    pass


def on_unmounting(fixture: Fixture):
    pass


def _call_error():
    raise ValueError("invalid call")
