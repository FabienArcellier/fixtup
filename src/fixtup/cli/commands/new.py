import os

import click

from fixtup.entity.fixture import Fixture
from fixtup.logger import get_logger
from fixtup.plugin import event
from fixtup.plugin.factory import lookup_plugin
from fixtup.prompt.factory import lookup_prompt
from fixtup.scaffold.base import scaffold_new_fixture
from fixtup.settings import read_settings


@click.command(help="Scaffold a new fixture")
def new() -> None:
    """
    scaffolding command that will generate a new fixture
    """
    settings = read_settings()

    prompt = lookup_prompt()
    fixture_id = prompt.new_fixture(settings.fixtures_dir)
    shared_fixture = prompt.confirm('Is this fixture is shared between all the tests ? ')

    # output
    fixture = Fixture.create_from_cli(fixture_id, settings.fixtures_dir, shared_fixture)

    plugin = lookup_plugin()
    plugin.invoke(event.BEFORE_SCAFFOLD_NEW_FIXTURE, fixture=fixture)
    scaffold_new_fixture(fixture)
    plugin.invoke(event.SCAFFOLD_NEW_FIXTURE, fixture=fixture)
