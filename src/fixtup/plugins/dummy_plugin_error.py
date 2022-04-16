import io
import os

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate


def on_new_fixture(template: FixtureTemplate):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'new_fixture.txt'), 'w') as file:
        file.write('')


def on_mounting(fixture: Fixture):
    for i in range(0, 10, 1):
        _call_error()


def on_starting(fixture: Fixture):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'starting.txt'), 'w') as file:
        file.write('')


def on_stopping(fixture: Fixture):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'stopping.txt'), 'w') as file:
        file.write('')


def on_unmounting(fixture: Fixture):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'unmounting.txt'), 'w') as file:
        file.write('')


def _call_error():
    raise ValueError("invalid call")
