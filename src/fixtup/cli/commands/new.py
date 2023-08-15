import click

from fixtup.context import lib_context_setup, lib_context
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.prompt.factory import lookup_prompt
from fixtup.scaffold.base import scaffold_new_fixture
from fixtup.settings.base import load_settings


@click.command(help="Scaffold a new fixture")
def new() -> None:
    """
    scaffolding command that will generate a new fixture
    """
    lib_context_setup()
    load_settings()

    prompt = lookup_prompt()

    fixtup_context = lib_context()

    fixture_id = prompt.new_fixture(fixtup_context.fixturesdir) # type: ignore

    # output
    template = FixtureTemplate.create_from_cli(fixture_id, fixtup_context.fixturesdir) # type: ignore
    scaffold_new_fixture(template)
