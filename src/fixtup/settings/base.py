import os
from typing import Optional

from fixtup.entity.settings import Settings
from fixtup.exceptions import PythonManifestMissing, FixtupSettingsMissing
from fixtup.settings.factory import lookup_parsers


class SettingsParser:

    def has_manifest(self, path: str) -> bool:
        """
        check if the manifest exists in the current path
        """
        raise NotImplementedError

    def contains_settings(self, path: str) -> bool:
        raise NotImplementedError

    def read_settings(self, path: str) -> Settings:
        raise NotImplementedError

    def append_settings(self, path: str, settings: Settings):
        raise NotImplementedError


def read_settings() -> Settings:
    """
    Read the settings of fixtup into the python project manifest

    :return:
    """
    starting_path = os.getcwd()
    parsers = lookup_parsers()
    path = starting_path
    is_python_project = False
    while os.path.dirname(path) != path:
        for parser in parsers:
            if parser.has_manifest(path):
                is_python_project = True
                if parser.contains_settings(path):
                    return parser.read_settings(path)

        path = os.path.dirname(path)

    if is_python_project is False:
        raise PythonManifestMissing("not a python project (or any of the parent directories): setup.cfg or pyproject.toml")

    raise FixtupSettingsMissing("fixtup not configured in this project, you should run fixtup init")

def write_settings(settings: Settings):
    """
    Write the settings to the existing project manifest

    ouvre le manifest projet et écrit à la fin la configuration

    :param manifest_path: the path of the python project manifest that may be setup.cfg or pyproject.toml
    :param settings: the default settings
    :return:
    """
    raise NotImplementedError()
