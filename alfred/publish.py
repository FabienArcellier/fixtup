import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("publish:dist", help="build distribution packages")
def publish__dist():
    """
    build distribution packages

    >>> $ alfred publish:dist
    """
    python = alfred.sh("python", "python should be present")
    os.chdir(ROOT_DIR)
    alfred.run(python, ['setup.py', 'bdist_wheel', 'sdist'])
