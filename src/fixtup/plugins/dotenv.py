import copy
import os
import shutil

from dotenv import load_dotenv

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.prompt.factory import lookup_prompt

store = {}


def on_new_fixture(template: FixtureTemplate):
    prompt = lookup_prompt()
    override_environment = prompt.confirm('Mount environment variables on this fixture')
    if override_environment:
        RESOURCE_DIR = os.path.realpath(os.path.join(__file__, '..', 'resource'))
        shutil.copy(os.path.join(RESOURCE_DIR, 'dotenv', '.env'), os.path.join(template.directory, '.env'))


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
