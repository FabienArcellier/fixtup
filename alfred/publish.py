import importlib.metadata
import os
import sys
from typing import Optional

import alfred
import click
from click import UsageError, Choice
from plumbum.commands.processes import ProcessExecutionError

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))

@alfred.command("publish", help="tag a new release and trigger pypi publication")
def publish():
    """
    tag a release through github actions

    >>> $ alfred publish
    """
    import fixtup
    VERSION = importlib.metadata.version(fixtup.__name__)

    git = alfred.sh("git", "git should be present")
    os.chdir(ROOT_DIR)

    # update the existing tags
    alfred.run(git, ["fetch"])

    current_version: Optional[str] = None
    try:
        current_version = git["describe", "--tags", "--abbrev=0"]().strip()
    except ProcessExecutionError as exception:
        # happens when no tag exists yet
        if "fatal: No names found, cannot describe anything." in exception.stderr:
            current_version = None
        else:
            raise
    git_status: str = git["status"]()

    on_master = "On branch master" in git_status
    if not on_master:
        click.echo(click.style("Branch should be on master, use git checkout master", fg="red"))
        click.echo(git_status.strip()[0])
        sys.exit(1)

    up_to_date = "Your branch is up to date with 'origin/master'" in git_status
    if not up_to_date:
        click.echo(click.style("Branch should be up to date with origin/master, push your change to repository", fg="red"))
        sys.exit(1)

    non_commited_changes = "Changes not staged for commit" in git_status or "Changes to be committed" in git_status
    if non_commited_changes:
        click.echo(click.style("Changes in progress, can't release a new version", fg="red"))
        sys.exit(1)

    if current_version == VERSION:
        click.echo(click.style(f"Version {VERSION} already exists, update version in pyproject.toml", fg='red'))
        sys.exit(1)

    click.echo("")
    click.echo(f"Next release {VERSION} (current: {current_version})")
    click.echo("")
    value = click.prompt("Confirm", type=Choice(['y', 'n']), show_choices=True, default='n')

    if value == 'y':
        alfred.run(git, ['tag', VERSION])
        alfred.run(git, ['push', 'origin', VERSION])


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
