import io
import os
import shutil

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.prompt.factory import lookup_prompt


def on_new_fixture(template: FixtureTemplate):
    prompt = lookup_prompt()
    mount_containers = prompt.confirm('Is this fixture mount docker containers ?')
    if mount_containers:
        RESOURCE_DIR = os.path.realpath(os.path.join(__file__, '..', 'resource'))
        shutil.copy(os.path.join(RESOURCE_DIR, 'docker', 'docker-compose.yml'), os.path.join(template.directory, 'docker-compose.yml'))


def on_mounting(fixture: Fixture):
    pass


def on_starting(fixture: Fixture):
    pass


def on_stopping(fixture: Fixture):
    pass


def on_unmounting(fixture: Fixture):
    pass
