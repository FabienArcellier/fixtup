import io
import os
import subprocess
import sys
from typing import Optional

from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.exceptions import HookRuntimeError
from fixtup.hook.base import HookEngine, HookEvent
from fixtup.lib.env import env_override
from fixtup.logger import get_logger


class PythonHookEngine(HookEngine):

    def run(self, event: HookEvent, template: FixtureTemplate) -> None:
        logger = get_logger()
        hook_directory = os.path.join(template.directory, '.hooks')
        if not os.path.isdir(hook_directory):
            logger.debug(f"fixture {template.identifier} does not expose hook directory in {hook_directory}")
            return

        _script = script(event)
        assert _script is not None, f"{event} is not implemented"

        hook_script = os.path.join(template.directory, _script)
        if not os.path.isfile(hook_script):
            logger.debug(
                f"fixture {template.identifier} does not expose hook script for event {event.value} - {hook_script}")
            return

        with env_override({
            "FIXTURE_IDENTIFIER": template.identifier
        }):
            """
            I decided to make a subprocess invocation for debug mode support instead
            than using an exec statement.


            If a developper set a breakpoint in its hook script, the python interpreter
            will stop on the breakpoint. This behavior makes it easier to debug a hook.
            """
            try:
                subprocess.check_call([sys.executable, hook_script])
            except subprocess.CalledProcessError as exception:
                raise HookRuntimeError("Error on hook invocation",
                                       template=template,
                                       hook_event=event,
                                       hook_script=hook_script)


def script(event: 'HookEvent') -> Optional[str]:
    files = {
        HookEvent.setup_data: os.path.join(".hooks", "hook_setup_data.py"),
        HookEvent.starting: os.path.join(".hooks", "hook_started.py"),
        HookEvent.stopping: os.path.join(".hooks", "hook_stopping.py"),
        HookEvent.teardown_data: os.path.join(".hooks", "hook_teardown_data.py"),
    }

    return files.get(event, None)
