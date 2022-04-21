import os

from click import UsageError
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


@alfred.command("publish:pypi", help="workflow to release fixtup to pypi")
def publish__dist():
    """
    workflow to release fixtup current version to pypi

    >>> $ alfred publish:pypi
    """
    alfred.invoke_command('dist')
    alfred.invoke_command('publish:twine')


@alfred.command("publish:twine", help="push fixtup to pypi")
def publish__twine():
    """
    push fixtup to pypi

    This operation requires you set a pypi publication token as env var

    * TWINE_USERNAME
    * TWINE_PASSWORD

    >>> $ alfred publish:twine
    """
    username = os.getenv('TWINE_USERNAME', None)
    password = os.getenv('TWINE_PASSWORD', None)
    if username is None:
        os.environ['TWINE_USERNAME'] = '__token__'

    if password is None:
        raise UsageError('TWINE_PASSWORD should contains your pypi token to publish fixtup : https://pypi.org/help/#apitoken')

    twine = alfred.sh("twine")
    os.chdir(ROOT_DIR)
    alfred.run(twine, ['upload', '--non-interactive', 'dist/*'])
