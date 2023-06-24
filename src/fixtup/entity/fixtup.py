import os
import tempfile
from typing import Optional, List

import attr
import platformdirs

class Driver:
    mock = 'mock'
    prompt_toolkit = 'prompt-toolkit'

@attr.s
class Fixtup:

    # Global settings
    appname: str = 'fixtup'
    appdir: Optional[str] = None
    mountdir: Optional[str] = None
    pid_owner: Optional[int] = None

    driver_prompt: str = Driver.prompt_toolkit
    enable_hooks: bool = True
    enable_plugins: bool = True

    # Each time fixtup.up is invoked, fixtup restarts as if it were a new test run. This mode is necessary to test some workflows in the automatic tests which requires a completely blank fixtup context
    emulate_new_process: bool = False


    # Project settings
    projectloaded: bool = False
    projectdir: Optional[str] = None
    manifestpath: Optional[str] = None
    fixturesdir: Optional[str] = None
    plugins: List[str] = attr.ib(factory=list)

    def __post_init__(self):
        if self.appdir is None:
            self.appdir = platformdirs.user_data_dir(self.appname, self.appname)

        if self.mountdir is None:
            self.mountdir = tempfile.gettempdir()

        self.pid_owner = os.getpid()
