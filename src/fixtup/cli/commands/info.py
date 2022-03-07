import click
from click.exceptions import ClickException

from fixtup.exceptions import FixtupException
from fixtup.settings.base import read_settings


@click.command(help="Display fixtup configuration information")
def info():
    try:
        settings = read_settings()
        click.echo(f"Configuration: {settings.manifest_path}")
        click.echo(f"Fixtures: {settings.fixtures_dir}")
        click.echo(f"Plugins:")
        for plugin in settings.plugins:
            click.echo(f"  * {plugin}")

        exit(0)
    except FixtupException as exception:
        raise ClickException(exception.msg) from exception
