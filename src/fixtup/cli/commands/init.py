import click

from fixtup.exceptions import FixtupSettingsMissing, PythonManifestMissing, FixtupException
from fixtup.prompt.factory import lookup_prompt
from fixtup.settings import read_settings
from fixtup.settings.base import list_project_manifests


@click.command(help="Init fixtup for a python project")
def init():
    if _is_fixtup_already_configured():
        click.echo("Fixtup is already configured, use fixtup info for more info")
        exit(2)

    try:
        prompt = lookup_prompt()
        available_manifests = list_project_manifests()
        fixture_repository = prompt.fixture_repository()
        manifest = prompt.choice(f"Python manifest {available_manifests} ?", available_manifests)

        # manifest_path = manifest_path(manifest)
        # settings = Settings.default_settings_for_init(manifest_path, fixture_repository)
        # create_fixture_repository(settings)
        # write_settings(settings)
    except FixtupException as exception:
        click.echo(exception.msg)
        exit(1)


def _is_fixtup_already_configured() -> bool:
    try:
        read_settings()
        return True
    except (FixtupSettingsMissing, PythonManifestMissing) as exception:
        return False
