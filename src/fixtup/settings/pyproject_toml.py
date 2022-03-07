import io
import os

import toml

from fixtup.entity.settings import Settings
from fixtup.logger import get_logger
from fixtup.settings.base import SettingsParser, RESOURCE_DIR

logger = get_logger()


class PyprojectToml(SettingsParser):
    manifest = "pyproject.toml"

    def has_manifest(self, path: str) -> bool:
        """
        check if the manifest pyproject.toml exists in the current path

        :param path: the directory that may contain the manifest pyproject.toml
        """
        manifest_expected_path = self._manifest_expected_path(path)
        manifest_exists = os.path.isfile(manifest_expected_path)

        if manifest_exists:
            logger.debug(f'manifest pyproject.toml is present : {manifest_expected_path}')

        return manifest_exists

    def contains_settings(self, path: str) -> bool:
        """
        Check if the section "tools.fixtup" is present in the manifest pyproject.toml

        :param path: the directory that contains the manifest pyproject.toml
        """
        manifest_expected_path = self._manifest_expected_path(path)
        self._assert_manifest_exists(manifest_expected_path)

        with io.open(manifest_expected_path) as file_pointer:
            global_settings = toml.load(file_pointer)
            return "tools" in global_settings and "fixtup" in global_settings["tools"]

    def read_settings(self, path: str) -> Settings:
        """
        Read the settings present in the manifest pyproject.toml.
        The section "tools.fixtup" has to be present.

        :param path: the directory that contains the manifest pyproject.toml
        """

        manifest_expected_path = self._manifest_expected_path(path)
        self._assert_manifest_exists(manifest_expected_path)

        with io.open(manifest_expected_path) as file_pointer:
            global_settings = toml.load(file_pointer)
            settings = global_settings["tools"]["fixtup"]
            return Settings.from_manifest(manifest_expected_path, settings)

    def append_settings(self, settings: Settings):
        """
        write the settings at the end of the manifres
        """
        manifest_expected_path = self._manifest_expected_path(settings.configuration_dir)
        self._assert_manifest_exists(manifest_expected_path)

        with io.open(os.path.join(RESOURCE_DIR, 'pyproject_toml_settings.in')) as file_pointer:
            pyproject_append_settings = file_pointer.read()

        pyproject_append_settings = pyproject_append_settings\
            .replace("{{ fixtures }}", settings.fixtures)

        with io.open(manifest_expected_path, mode="a") as file_pointer:
            file_pointer.write(pyproject_append_settings)

    def _assert_manifest_exists(self, manifest_expected_path):
        assert os.path.isfile(manifest_expected_path), \
            f"use has_manifest method to check manifest if manifest exists: {manifest_expected_path}"

    def _manifest_expected_path(self, path):
        manifest_expected_path = os.path.abspath(os.path.join(path, 'pyproject.toml'))
        return manifest_expected_path
