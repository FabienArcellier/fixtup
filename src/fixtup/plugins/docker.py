import os
import warnings
from typing import Optional, Union

import plumbum
from plumbum.commands.base import BaseCommand
import shutil

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.os import is_posix, is_windows
from fixtup.prompt.factory import lookup_prompt


# I have no idea how to remove the warning message except by
# removing them when loading the module
warnings.simplefilter("ignore", ResourceWarning)

# Cache for the detected docker compose command
_docker_compose_cmd: Optional[BaseCommand] = None


def on_new_fixture(template: FixtureTemplate):
    prompt = lookup_prompt()
    mount_containers = prompt.confirm('Mount docker container on this fixture')
    if mount_containers:
        RESOURCE_DIR = os.path.realpath(os.path.join(__file__, '..', 'resource'))
        shutil.copy(os.path.join(RESOURCE_DIR, 'docker', 'docker-compose.yml'), os.path.join(template.directory, 'docker-compose.yml'))


def on_starting(fixture: Fixture):
    if _is_docker_compose_absent(fixture):
        return

    docker_compose = get_docker_compose_cmd()
    cmd = docker_compose['up', '--no-start', '--remove-orphans']
    exit_code, stdout, stderr = cmd.run()
    if exit_code != 0:
        raise OSError(stderr)

    docker_compose = get_docker_compose_cmd()
    cmd = docker_compose['up', '--detach']
    cmd()


def on_stopping(fixture: Fixture):
    if _is_docker_compose_absent(fixture):
        return

    docker_compose = get_docker_compose_cmd()
    cmd = docker_compose['stop']
    cmd()

    # I would prefer to run the docker-compose logs in a separate thread
    # to view the log of the container during debug. I will think about
    # a way to do that.
    if os.getenv('FIXTUP_DOCKER_VERBOSE', None) is not None:
        cmd = docker_compose['logs', '--timestamps']
        cmd & plumbum.FG

    docker_compose = get_docker_compose_cmd()
    cmd = docker_compose['down']
    cmd()




def _is_docker_compose_absent(fixture: Fixture):
    return not os.path.isfile(os.path.join(fixture.directory, 'docker-compose.yml'))


def _is_docker_compose_v2_available() -> bool:
    """
    Check if Docker Compose V2 plugin is available (docker compose).
    
    Returns True if `docker compose` command is available, False otherwise.
    """
    try:
        # Try to run 'docker compose version' to check if V2 is available
        docker = plumbum.local['docker']
        result = docker['compose', 'version'].run(retcode=None)
        return result[0] == 0
    except Exception:
        return False


def _is_docker_compose_v1_available() -> bool:
    """
    Check if Docker Compose V1 standalone is available (docker-compose).
    
    Returns True if `docker-compose` command is available, False otherwise.
    """
    try:
        if is_windows():
            plumbum.local['docker-compose.exe']
        else:
            plumbum.local['docker-compose']
        return True
    except Exception:
        return False


def _detect_docker_compose_cmd() -> BaseCommand:
    """
    Detect and return the appropriate docker compose command.
    
    Priority:
    1. Docker Compose V2 plugin (docker compose) - preferred for modern installations
    2. Docker Compose V1 standalone (docker-compose) - fallback for legacy installations
    
    Raises:
        OSError: If neither docker compose command is available.
    """
    # Check for Docker Compose V2 first (modern installations)
    if _is_docker_compose_v2_available():
        docker = plumbum.local['docker']
        return docker['compose']
    
    # Fall back to Docker Compose V1 (legacy installations)
    if _is_docker_compose_v1_available():
        if is_windows():
            return plumbum.local['docker-compose.exe']
        return plumbum.local['docker-compose']
    
    raise OSError(
        "Neither 'docker compose' (V2) nor 'docker-compose' (V1) is available. "
        "Please install Docker Compose."
    )


def get_docker_compose_cmd() -> BaseCommand:
    """
    Get the docker compose command.
    
    The command is detected once and cached for subsequent calls.
    
    Returns:
        BaseCommand: The detected docker compose command (either V1 or V2).
    """
    global _docker_compose_cmd
    
    if _docker_compose_cmd is None:
        _docker_compose_cmd = _detect_docker_compose_cmd()
    
    return _docker_compose_cmd


def reset_docker_compose_cmd() -> None:
    """
    Reset the cached docker compose command.
    
    This is useful for testing purposes to force re-detection.
    """
    global _docker_compose_cmd
    _docker_compose_cmd = None
