import io
import os

import yaml

from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.exceptions import FixtureNotFound
from fixtup.logger import get_logger
from fixtup.settings import read_settings


def fixture_template(identifier: str) -> FixtureTemplate:
    settings = read_settings()
    fixtures_path = settings.fixtures_dir
    fixture_template = _fixture_template_path(fixtures_path, identifier)
    config = _read_fixture_yml(fixture_template)
    return FixtureTemplate.create_from_fixture_template(fixture_template, config)


def _fixture_template_path(fixtures_path, fixture):
    fixture_template = os.path.join(fixtures_path, fixture)
    if not os.path.isdir(fixture_template):
        fixtures_list = [d for d in os.listdir(fixtures_path) if
                         os.path.isdir(os.path.join(fixtures_path, d))]
        raise FixtureNotFound('the fixture {0} does not exists in fixtures : {1}'.format(fixture, fixtures_list))
    return fixture_template


def _read_fixture_yml(fixture_template: str) -> dict:
    """
    lit le fichier de configuration fixture.yml dans le template de la
    fixture

    >>> config = _read_fixture_yml("/home/far/hello/fixtup/fixture/my_simple_env")
    :param fixture_template: le dossier du template de la fixture
    """
    logger = get_logger()
    fixture_yml = os.path.join(fixture_template, 'fixtup.yml')
    try:
        if os.path.isfile(fixture_yml):
            with io.open(fixture_yml) as filepointer:
                config = yaml.load(filepointer, Loader=yaml.SafeLoader)
            return config
    except Exception as exception:
        logger.exception(f"fail to load & parse {fixture_yml} - {exception}")

    return {}
