import click

from fixtup.entity.settings import Settings
from fixtup.exceptions import FixtupSettingsMissing, PythonManifestMissing, FixtupException
from fixtup.prompt.factory import lookup_prompt
from fixtup.scaffold.base import scaffold_fixture_repository
from fixtup.settings import read_settings
from fixtup.settings.base import list_project_manifests, write_settings


@click.command(help="Init fixtup for a python project")
def init():
    if _is_fixtup_already_configured():
        click.echo("Fixtup is already configured, use fixtup info for more info")
        exit(2)

    try:
        prompt = lookup_prompt()
        available_manifests = list_project_manifests()
        fixture_repository = prompt.fixture_repository()
        manifest_choice = prompt.choice(f"Python manifest",
                                        available_manifests.prompt_choices())

        picked_manifest = available_manifests.get(manifest_choice)
        settings = Settings.default_settings_for_init(picked_manifest, fixture_repository)
        scaffold_fixture_repository(settings)
        write_settings(settings)
    except FixtupException as exception:
        click.echo(exception.msg)
        exit(1)


def _is_fixtup_already_configured() -> bool:
    try:
        read_settings()
        return True
    except (FixtupSettingsMissing, PythonManifestMissing) as exception:
        return False
