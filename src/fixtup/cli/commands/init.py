import click

from fixtup.entity.settings import Settings
from fixtup.exceptions import FixtupSettingsMissing, PythonManifestMissing
from fixtup.prompt.factory import lookup_prompt
from fixtup.settings import read_settings


@click.command(help="Init fixtup for a python project")
def init():
    if _is_fixtup_already_configured():
        click.echo("Fixtup is already configured, use fixtup info for more info")
        exit(2)

    prompt = lookup_prompt()
    fixture_repository = prompt.fixture_repository()
    #
    # available_manifests: List[str] = list_manifests()
    # manifest = prompt.choice(available_manifests)
    # settings = Settings.default_settings_for_init(manifest, fixture_repository)
    # create_fixture_repository(settings)
    # write_settings(settings)


def _is_fixtup_already_configured() -> bool:
    try:
        read_settings()
        return True
    except (FixtupSettingsMissing, PythonManifestMissing) as exception:
        return False
