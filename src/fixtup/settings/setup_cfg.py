import os

import configparser

from fixtup.entity.settings import Settings
from fixtup.logger import get_logger
from fixtup.settings.base import SettingsParser


logger = get_logger()


class SetupCfg(SettingsParser):
    def has_manifest(self, path: str) -> bool:
        """
        check if the manifest pyproject.toml exists in the current path

        :param path: the directory that may contain the manifest setup.cfg
        """
        manifest_expected_path = self._manifest_expected_path(path)
        manifest_exists = os.path.isfile(manifest_expected_path)

        if manifest_exists:
            logger.debug(f'manifest pyproject.toml is present : {manifest_expected_path}')

        return manifest_exists

    def contains_settings(self, path: str) -> bool:
        """
        Check if the section "tools.fixtup" is present in the manifest setup.cfg

        :param path: the directory that contains the manifest setup.cfg
        """
        manifest_expected_path = self._manifest_expected_path(path)
        self._assert_manifest_exists(manifest_expected_path)

        parser = configparser.ConfigParser()
        parser.read(manifest_expected_path)

        return "fixtup" in parser

    def read_settings(self, path: str) -> Settings:
        """
        Read the settings present in the manifest setup.cfg
        The section "tools.fixtup" has to be present.

        :param path: the directory that contains the manifest setup.cfg
        """
        manifest_expected_path = self._manifest_expected_path(path)
        self._assert_manifest_exists(manifest_expected_path)

        parser = configparser.ConfigParser()
        parser.read(manifest_expected_path)

        return Settings.from_manifest(path, dict(parser["fixtup"]))

    def append_settings(self, path: str, settings: Settings):
        pass

    def _assert_manifest_exists(self, manifest_expected_path):
        assert os.path.isfile(manifest_expected_path), \
            f"use has_manifest method to check manifest if manifest exists: {manifest_expected_path}"

    def _manifest_expected_path(self, path):
        manifest_expected_path = os.path.abspath(os.path.join(path, 'setup.cfg'))
        return manifest_expected_path
