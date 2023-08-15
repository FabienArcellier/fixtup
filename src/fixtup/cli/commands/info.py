import click
from click.exceptions import ClickException

from fixtup.context import lib_context, lib_context_setup
from fixtup.exceptions import FixtupException
from fixtup.settings.base import load_settings


@click.command(help="Display fixtup configuration information")
def info():
    try:
        lib_context_setup()
        load_settings()
        fixtup_context = lib_context()
        click.echo(f"Configuration: {fixtup_context.manifestpath}")
        click.echo(f"Fixtures: {fixtup_context.fixturesdir}")
        click.echo(f"Plugins:")
        for plugin in fixtup_context.plugins:
            click.echo(f"  * {plugin}")

        exit(0)
    except FixtupException as exception:
        raise ClickException(exception.msg) from exception
