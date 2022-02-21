import click

from fixtup.settings.base import read_settings


@click.command(help="Display fixtup informations")
def info():
    settings = read_settings()
    click.echo(f"Fixtures: {settings.fixtures_dir}")
    exit(0)
