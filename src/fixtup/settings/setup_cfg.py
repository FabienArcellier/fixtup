import io
import os

import configparser

from fixtup.entity.settings import Settings
from fixtup.logger import get_logger
from fixtup.settings.base import SettingsParser, RESOURCE_DIR


logger = get_logger()


class SetupCfg(SettingsParser):
    manifest = "setup.cfg"

    def has_manifest(self, path: str) -> bool:
        """
        check if the manifest pyproject.toml exists in the current path

        :param path: the directory that may contain the manifest setup.cfg
        """
        manifest_expected_path = self._manifest_expected_path(path)
        manifest_exists = os.path.isfile(manifest_expected_path)

        if manifest_exists:
            logger.debug(f'manifest setup.cfg is present : {manifest_expected_path}')

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

        settings = parser["fixtup"]
        _settings = _parse(settings)

        return Settings.from_manifest(manifest_expected_path, _settings)

    def append_settings(self, settings: Settings):
        """
        write the settings at the end of the manifest
        """
        manifest_expected_path = self._manifest_expected_path(settings.configuration_dir)
        self._assert_manifest_exists(manifest_expected_path)

        with io.open(os.path.join(RESOURCE_DIR, 'setup_cfg_settings.in')) as file_pointer:
            setup_cfg_content = file_pointer.read()

        setup_cfg_content = setup_cfg_content\
            .replace("{{ fixtures }}", settings.fixtures)

        with io.open(manifest_expected_path, mode="a") as file_pointer:
            file_pointer.write(setup_cfg_content)

    def _assert_manifest_exists(self, manifest_expected_path):
        assert os.path.isfile(manifest_expected_path), \
            f"use has_manifest method to check manifest if manifest exists: {manifest_expected_path}"

    def _manifest_expected_path(self, path):
        manifest_expected_path = os.path.abspath(os.path.join(path, 'setup.cfg'))
        return manifest_expected_path


def _parse(settings: configparser.SectionProxy) -> dict:
    output: dict = {}
    for attribute in settings:
        value = settings[attribute]

        # if value content match the pattern of a list
        # `\nvalue1\nvalue2
        if value.startswith('\n'):
            output[attribute] = value[1:].split('\n')
            continue

        output[attribute] = settings[attribute]

    return output
