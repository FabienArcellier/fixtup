import os

import alfred
import click

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))


@alfred.command("tests", help="workflow to execute all automatic tests")
def tests():
    """
    workflow to execute all automatic tests

    >>> $ alfred tests
    """
    alfred.invoke_command('tests:units')
    alfred.invoke_command('tests:integrations')
    alfred.invoke_command('tests:acceptances')


@alfred.command("tests:acceptances", help="execute acceptances tests")
def tests_acceptances():
    """
    execute acceptances tests with unittests

    >>> $ alfred tests:acceptances
    """
    python = alfred.sh("python")
    os.chdir(ROOT_DIR)
    alfred.run(python, ['-m', 'unittest', 'discover', 'tests/acceptances'])


@alfred.command("tests:integrations", help="execute integrations tests")
def tests_integrations():
    """
    execute integrations tests with unittests

    >>> $ alfred tests:integrations
    """
    python = alfred.sh("python")
    os.chdir(ROOT_DIR)
    alfred.run(python, ['-m', 'unittest', 'discover', 'tests/integrations'])


@alfred.command("tests:units", help="execute unit tests")
def tests_units():
    """
    execute unit tests with unittests

    >>> $ alfred tests:units
    """
    python = alfred.sh("python")
    os.chdir(ROOT_DIR)
    alfred.run(python, ['-m', 'unittest', 'discover', 'tests/units'])

