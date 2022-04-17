import contextlib

from fixtup.entity.settings import Settings
from fixtup.settings.module import configure_from_code, reset_settings


@contextlib.contextmanager
def override_fixtup_settings(settings: dict):
    """
    context to overrides the settings of fixtup for a test.

    >>> with override_fixtup_settings({
    >>>        "fixtures": os.path.join(SCRIPT_DIR, "../fixtures/fixtup"),
    >>>        'plugins': [
    >>>            'fixtup.plugins.dummy_plugin_error'
    >>>        ]
    >>>    }):
    >>>     with fixtup.up('simple'):
    >>>         cwd = os.getcwd()

    It's useful to activate or deactivate plugins in acceptance tests
    """
    _settings = Settings.from_configuration(settings)
    configure_from_code(_settings)
    yield
    reset_settings()


