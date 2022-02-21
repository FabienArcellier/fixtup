import click
from click.exceptions import Abort, ClickException

from fixtup.exceptions import FixtupException
from fixtup.settings.base import read_settings


@click.command(help="Display fixtup informations")
def info():
    try:
        settings = read_settings()
        click.echo(f"Configuration: {settings.configuration_path}")
        click.echo(f"Fixtures: {settings.fixtures_dir}")
        exit(0)
    except FixtupException as exception:
        raise ClickException(exception.msg) from exception
