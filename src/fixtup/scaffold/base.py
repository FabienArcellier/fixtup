import io
import os
import shutil

from jinja2 import Environment
import yaml

from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.entity.plugin import PluginEvent
from fixtup.entity.settings import Settings
from fixtup.logger import get_logger
from fixtup.plugin.factory import lookup_plugin_engine

RESOURCE_DIR = os.path.realpath(os.path.join(__file__, '..', 'resource'))


def scaffold_fixture_repository(settings: Settings):
    """

    >>> settings = Settings.from_manifest("/home/far/hello/setup.cfg", {})
    >>> scaffold_fixture_repository(settings)

    :param settings:
    :return:
    """
    logger = get_logger()
    logger.debug(f'scaffold fixture repository: {settings.fixtures_dir}')
    os.makedirs(settings.fixtures_dir)


def scaffold_new_fixture(fixture: FixtureTemplate):
    """
    :param fixture: the fixture definition
    :return:
    """
    logger = get_logger()
    logger.debug(f'scaffold new fixture: {fixture}')
    os.makedirs(fixture.directory)

    _generate_fixtup_manifest(fixture)
    _generate_hooks_directory(fixture)

    plugin = lookup_plugin_engine()
    plugin.run(PluginEvent.new_fixture, template = fixture)


def _generate_hooks_directory(fixture: FixtureTemplate):
    template = os.path.join(RESOURCE_DIR, 'hooks')
    target = os.path.join(fixture.directory, '.hooks')
    shutil.copytree(template, target)


def _generate_fixtup_manifest(fixture: FixtureTemplate):
    template = os.path.join(RESOURCE_DIR, 'fixtup.yml.j2')
    target = os.path.join(fixture.directory, 'fixtup.yml')
    with io.open(template) as file_pointer:
        fixtup_manifest_tpl = file_pointer.read()

    fixtup_manifest = _render(fixtup_manifest_tpl, fixture.variables())
    with io.open(target, 'w') as file_pointer:
        file_pointer.write(fixtup_manifest)


def _render(content: str, variables: dict) -> str:
    env = Environment()
    tmpl = env.from_string(content)
    return tmpl.render(**variables)
