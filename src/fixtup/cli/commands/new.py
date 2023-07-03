import os

import click

from fixtup import context
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.prompt.factory import lookup_prompt
from fixtup.scaffold.base import scaffold_new_fixture
from fixtup.settings.base import load_settings_into_ctx


@click.command(help="Scaffold a new fixture")
def new() -> None:
    """
    scaffolding command that will generate a new fixture
    """
    fixtup_context = context.up()
    load_settings_into_ctx(fixtup_context)

    prompt = lookup_prompt()

    fixture_id = prompt.new_fixture(fixtup_context.fixturesdir) # type: ignore

    # output
    template = FixtureTemplate.create_from_cli(fixture_id, fixtup_context.fixturesdir) # type: ignore
    scaffold_new_fixture(template)
