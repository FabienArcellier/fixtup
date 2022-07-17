import os
from contextlib import contextmanager
from typing import Generator, List, Union

from fixtup.entity.settings import Settings
from fixtup.fixture.factory import lookup_fixture_engine
from fixtup.fixture_template.base import fixture_template
from fixtup.logger import get_logger
from fixtup.settings.module import configure_from_code

logger = get_logger()

current_working_dir = None


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
def up(fixture: str, keep_mounted_fixture: bool = False) -> Generator[None, None, None]:
    """
    Mount a fixture to use it in a test.

    The mounted fixture is removed either at when the context is closed, either when the python process
    has finished to run depending of the fixture policy.

    If you want to keep the mounted context to debug the impact of the code inside
    the mounted fixture, set `keep_mounted_fixture` at True.

    >>> with fixtup.up('thumbnail_context'):
    >>>     os.chdir(wd)
    >>>     # do something ...

    :param fixture: the identifier of the fixture, it's the name of the directory that define the fixture
    :param keep_mounted_fixture: don't remove the directory of mounted fixture at the end of the context
    """

    # If we load 2 fixtures one after the other, the fixtup configuration is not recoverable
    # if we don't reset the working folder.
    #
    # >>> with fixtup.up('fixture1'):
    # >>>  with fixtup.up('fixture2'):
    #       ...
    #
    global current_working_dir
    if current_working_dir is None:
        highest_context = True
    else:
        highest_context = False

    if current_working_dir is not None:
        os.chdir(current_working_dir)

    fixture_engine = lookup_fixture_engine(highest_context=highest_context)
    template = fixture_template(fixture)

    current_working_dir = os.getcwd()

    try:
        with fixture_engine.run(template, keep_mounted_fixture=keep_mounted_fixture):
            yield

    finally:
        os.chdir(current_working_dir)
        if highest_context is True:
            current_working_dir = None
