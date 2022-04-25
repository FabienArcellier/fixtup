import os

import alfred
import click

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("ci", help="workflow to execute the continuous integration process")
@click.option("--no-docs", is_flag=True,help="ignore documentation in continuous integration")
def ci(no_docs: bool):
    """
    workflow to execute the continuous integration process

    * run the linter
    * run the automated tests beginning with units tests

    >>> $ alfred ci
    """
    alfred.invoke_command('lint')
    alfred.invoke_command('tests')

    if not no_docs:
        alfred.invoke_command('docs:check')


