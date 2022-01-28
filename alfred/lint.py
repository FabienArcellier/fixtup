import os

import alfred
import click

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))

@alfred.command("lint", help="check type consistency on source code")
def lint():
    """
    check the type consistency with mypy

    >>> $ alfred lint
    """
    mypy = alfred.sh("mypy", "mypy should be present")
    os.chdir(ROOT_DIR)
    alfred.run(mypy, ['src'])

