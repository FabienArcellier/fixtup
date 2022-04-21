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

    current_working_dir = os.getcwd()

    try:
        with fixture_engine.use(template, keep_mounted_fixture=keep_mounted_fixture) as fixture:
            with fixture_engine.run(template, fixture):
                yield
    finally:
        os.chdir(current_working_dir)
