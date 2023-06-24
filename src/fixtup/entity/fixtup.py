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

    # A chaque fois que fixtup.up est invoqué, fixtup redémarre comme si c'était une nouvelle exécution des
    # tests. Ce mode est nécessaire pour tester certains workflows dans les tests automatiques qui requiert un
    # contexte fixtup complètement vierge
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
