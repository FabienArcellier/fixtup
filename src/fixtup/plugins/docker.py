import os
import warnings

import plumbum
import shutil

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.prompt.factory import lookup_prompt


# I have no idea how to remove the warning message except by
# removing them when loading the module
warnings.simplefilter("ignore", ResourceWarning)


def on_new_fixture(template: FixtureTemplate):
    prompt = lookup_prompt()
    mount_containers = prompt.confirm('Mount docker container on this fixture')
    if mount_containers:
        RESOURCE_DIR = os.path.realpath(os.path.join(__file__, '..', 'resource'))
        shutil.copy(os.path.join(RESOURCE_DIR, 'docker', 'docker-compose.yml'), os.path.join(template.directory, 'docker-compose.yml'))


def on_starting(fixture: Fixture):
    if _is_docker_compose_absent(fixture):
        return

    docker_compose = plumbum.local['docker-compose']
    cmd = docker_compose['up', '--no-start', '--remove-orphans']
    exit_code, stdout, stderr = cmd.run()
    if exit_code != 0:
        raise OSError(stderr)

    docker_compose = plumbum.local['docker-compose']
    cmd = docker_compose['up', '--detach']
    cmd()


def on_stopping(fixture: Fixture):
    if _is_docker_compose_absent(fixture):
        return

    docker_compose = plumbum.local['docker-compose']
    cmd = docker_compose['stop']
    cmd()

    # I would prefer to run the docker-compose logs in a separate thread
    # to view the log of the container during debug. I will think about
    # a way to do that.
    if os.getenv('FIXTUP_DOCKER_VERBOSE', None) is not None:
        cmd = docker_compose['logs', '--timestamps']
        cmd & plumbum.FG

    docker_compose = plumbum.local['docker-compose']
    cmd = docker_compose['down']
    cmd()




def _is_docker_compose_absent(fixture: Fixture):
    return not os.path.isfile(os.path.join(fixture.directory, 'docker-compose.yml'))
