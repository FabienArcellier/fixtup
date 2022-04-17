import threading

from fixtup.entity.settings import Settings
from fixtup.logger import get_logger
from fixtup.settings.base import SettingsParser

logger = get_logger()

thread_store = threading.local()
thread_store.settings = None


def configure_from_code(settings: Settings):
    thread_store.settings = settings


def reset_settings():
    thread_store.settings = None


class ModuleSettings(SettingsParser):
    manifest = None

    def has_manifest(self, path: str) -> bool:
        """
        check if the module has been setup using `fixtup.configure`

        :param path: not used
        """
        return thread_store.settings is not None

    def contains_settings(self, path: str) -> bool:
        """
        check if the module has been setup using `fixtup.configure`

        :param path: not used
        """
        self._assert_settings_configured()
        return isinstance(thread_store.settings, Settings)

    def read_settings(self, path: str) -> Settings:
        """
        fetch the settings configured with `fixtup.configure`

        :param path: the directory that contains the manifest pyproject.toml
        """
        self._assert_settings_configured()
        return thread_store.settings

    def append_settings(self, settings: Settings):
        """
        not used
        """
        raise NotImplementedError("can not be implemented or used")

    def _assert_settings_configured(self):
        assert thread_store.settings is not None, \
            f"use has_manifest method to check the settings has been applied"
