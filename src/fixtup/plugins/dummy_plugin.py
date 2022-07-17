import io
import os

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate


def on_new_fixture(template: FixtureTemplate):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'new_fixture.txt'), 'w') as file:
        file.write('')


def on_setup_data(fixture: Fixture):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'setup_data.txt'), 'w') as file:
        file.write('')


def on_starting(fixture: Fixture):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'starting.txt'), 'w') as file:
        file.write('')


def on_stopping(fixture: Fixture):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'stopping.txt'), 'w') as file:
        file.write('')


def on_teardown_data(fixture: Fixture):
    directory = os.getcwd()
    with io.open(os.path.join(directory, 'teardown_data.txt'), 'w') as file:
        file.write('')

