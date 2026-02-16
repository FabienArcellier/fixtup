import os

import alfred
import click
from plumbum import local

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("ci", help="workflow to execute the continuous integration process")
@click.option("--no-docs", is_flag=True,help="ignore documentation in continuous integration")
@click.option("--no-docker", is_flag=True, help="disable the test suite using docker (for windows & macos on github action)")
def ci(no_docs: bool, no_docker: bool):
    """
    workflow to execute the continuous integration process

    * run the linter
    * run the automated tests beginning with units tests

    >>> $ alfred ci
    """
    ignore_docker_test = '1' if no_docker else '0'
    if ignore_docker_test:
        os.environ['IGNORE_DOCKER_TESTS'] = ignore_docker_test

    alfred.invoke_command('lint')
    alfred.invoke_command('tests')

    if not no_docs:
        alfred.invoke_command('docs:check')


