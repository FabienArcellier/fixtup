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
    appname: str = attr.ib(default='fixtup')
    appdir: Optional[str] = attr.ib(default=None)
    mountdir: Optional[str] = attr.ib(default=None)
    pid_owner: Optional[int] = attr.ib(default=None)

    driver_prompt: str = Driver.prompt_toolkit
    enable_hooks: bool = attr.ib(default=True)
    enable_plugins: bool = attr.ib(default=True)

    # Each time fixtup.up is invoked, fixtup restarts as if it were a new test run. This mode is necessary to test some workflows in the automatic tests which requires a completely blank fixtup context
    emulate_new_process: bool = attr.ib(default=False)


    # Project settings
    projectloaded: bool = attr.ib(default=False)
    projectdir: Optional[str] = attr.ib(default=None)
    manifestpath: Optional[str] = attr.ib(default=None)
    fixturesdir: Optional[str] = attr.ib(default=None)
    plugins: List[str] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        if self.appdir is None:
            self.appdir = platformdirs.user_data_dir(self.appname, self.appname)

        if self.mountdir is None:
            self.mountdir = tempfile.gettempdir()

        self.pid_owner = os.getpid()
