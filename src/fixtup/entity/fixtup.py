import os
import tempfile
from typing import Optional, List

import attr
import platformdirs


@attr.s
class Fixtup:

    # Global settings
    appname: str = 'fixtup'
    appdir: Optional[str] = None
    mountdir: Optional[str] = None
    pid_owner: Optional[int] = None

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
