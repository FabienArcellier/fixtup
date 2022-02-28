import logging
import os

import click

from fixtup.cli.commands.info import info
from fixtup.cli.commands.init import init
from fixtup.cli.commands.new import new
from fixtup.logger import get_logger

BASE_DIR = os.path.realpath(os.path.join(__file__, '..'))

@click.group()
@click.option('--verbose', '-v', is_flag=True, default=False, help='show detailled login')
def cli(verbose):

    if verbose:
        logging.basicConfig(format="%(message)s", level=logging.DEBUG)

cli.add_command(init)
cli.add_command(new)
cli.add_command(info)
