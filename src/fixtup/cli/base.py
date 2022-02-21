import os

import click

from fixtup.cli.commands.info import info
from fixtup.cli.commands.init import init
from fixtup.cli.commands.new import new

BASE_DIR = os.path.realpath(os.path.join(__file__, '..'))

@click.group()
def cli():
    pass

cli.add_command(init)
cli.add_command(new)
cli.add_command(info)
