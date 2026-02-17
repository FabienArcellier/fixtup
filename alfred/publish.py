import importlib.metadata
import os
import sys
from typing import Optional

import alfred
import click
from click import UsageError, Choice
from plumbum.commands.processes import ProcessExecutionError

import fixtup

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))
VERSION = importlib.metadata.version(fixtup.__name__)


@alfred.command("publish", help="tag a new release and trigger pypi publication")
def publish():
    """
    tag a release through github actions

    >>> $ alfred publish
    """
    git = alfred.sh("git", "git should be present")
    os.chdir(ROOT_DIR)

    # update the existing tags
    alfred.run(git, ["fetch"])

    current_version: Optional[str] = None
    try:
        current_version = alfred.run(git, ["describe", "--tags", "--abbrev=0"])[1].strip()
    except ProcessExecutionError as exception:
        # happens when no tag exists yet
        if "fatal: No names found, cannot describe anything." in exception.stderr:
            current_version = None
        else:
            raise
    git_status: str = alfred.run(git, ["status"])[1]

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
    poetry = alfred.sh("poetry", "poetry should be present")
    os.chdir(ROOT_DIR)
    alfred.run(poetry, ['build'])
    alfred.run(poetry, ['publish'])
