import os

import alfred
import click

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("ci", help="workflow to execute the continuous integration process")
def ci():
    """
    workflow to execute the continuous integration process

    * run the linter
    * run the automated tests beginning with units tests

    >>> $ alfred ci
    """
    alfred.invoke_command('lint')
    alfred.invoke_command('tests')


