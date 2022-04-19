import copy
import os

from dotenv import load_dotenv

from fixtup.entity.fixture import Fixture


store = {}


def on_starting(fixture: Fixture):
    if not _has_dotenv_file(fixture):
        return

    dotenv_path = os.path.join(fixture.directory, '.env')
    store['environ'] = copy.deepcopy(os.environ)
    load_dotenv(dotenv_path)


def on_stopping(fixture: Fixture):
    if not _has_dotenv_file(fixture):
        return

    os.environ = store['environ']
    del store['environ']


def _has_dotenv_file(fixture: Fixture) -> bool:
    dotenv_path = os.path.join(fixture.directory, '.env')
    return os.path.isfile(dotenv_path)
