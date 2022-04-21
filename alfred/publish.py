import os

import alfred

import fixtup

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("publish", help="tag a release of fixtup and release through github actions")
def publish():
    """
    tag a release of fixtup and release through github actions

    >>> $ alfred publish
    """
    git = alfred.sh("git", "git should be present")
    os.chdir(ROOT_DIR)
    alfred.run(git, ['tag', fixtup.__version__])
    alfred.run(git, ['push', 'origin', fixtup.__version__])


@alfred.command("publish:dist", help="build distribution packages")
def publish__dist():
    """
    build distribution packages

    >>> $ alfred publish:dist
    """
    python = alfred.sh("python", "python should be present")
    os.chdir(ROOT_DIR)
    alfred.run(python, ['setup.py', 'bdist_wheel', 'sdist'])
