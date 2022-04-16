import os
from contextlib import contextmanager
from typing import Generator

from fixtup.entity.settings import Settings
from fixtup.exceptions import FixtureNotFound
from fixtup.fixture.factory import lookup_fixture_engine
from fixtup.fixture_template.base import fixture_template
from fixtup.logger import get_logger
from fixtup.settings.module import configure_from_code

logger = get_logger()


def configure(settings: dict) -> None:
    """
    configure the module fixtup to override configuration

    You should prefer configure fixtup using
    python manifest like setup.cfg or pyproject.toml.

    >>> import os
    >>>
    >>> import fixtup
    >>>
    >>> SCRIPT_DIR = os.directory.realpath(os.directory.join(__file__, '..'))
    >>> fixtup.configure({"fixtures": os.directory.join(SCRIPT_DIR, "../fixtures")})

    :param settings: a key value dictionary that specify the settings of fixtup
    """
    _settings = Settings.from_configuration(settings)
    configure_from_code(_settings)


@contextmanager
def up(_fixture: str, keep_mounted_fixture: bool = False) -> Generator[None, None, None]:
    """
    Mount a fixture to use it in a test.

    The mounted fixture is removed either at when the context is closed, either when the python process
    has finished to run depending of the fixture policy.

    If you want to keep the mounted context to debug the impact of the code inside
    the mounted fixture, set `keep_mounted_fixture` at True.

    >>> with fixtup.up('thumbnail_context') as wd:
    >>>     os.chdir(wd)
    >>>     # do something ...

    :param _fixture: the identifier of the fixture, it's the name of the directory that define the fixture
    :param keep_mounted_fixture: don't remove the directory of mounted fixture at the end of the context
    """

    fixture_engine = lookup_fixture_engine()
    template = fixture_template(_fixture)
    fixture = fixture_engine.new_fixture(template)
    fixture_engine.mount(template, fixture)
    logger.debug(f'mount fixture directory: {fixture.directory}')

    current_working_dir = os.getcwd()
    os.chdir(fixture.directory)
    fixture_engine.start(template, fixture)
    logger.debug(f'start fixture: {fixture.directory}')

    try:
        yield
    finally:
        os.chdir(current_working_dir)
        logger.debug(f'stop fixture : {fixture.directory}')
        fixture_engine.stop(template, fixture)
        if not keep_mounted_fixture:
            logger.debug(f'remove mounted fixture directory : {fixture.directory}')
            fixture_engine.unmount(template, fixture)


def _fixture_template_path(fixtures_path, fixture):
    fixture_template = os.path.join(fixtures_path, fixture)
    if not os.path.isdir(fixture_template):
        fixtures_list = [d for d in os.listdir(fixtures_path) if
                         os.path.isdir(os.path.join(fixtures_path, d))]
        raise FixtureNotFound('the fixture {0} does not exists in fixtures : {1}'.format(fixture, fixtures_list))
    return fixture_template
