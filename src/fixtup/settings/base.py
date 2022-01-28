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

    raise FixtupSettingsMissing("no fixtup in this project, you should run fixtup init")

def write_settings(settings: Settings):
    """
    Write the settings to the existing project manifest

    Recherche depuis le working directory le manifest du projet (setup.cfg, pyproject.toml, ...) dans les dossiers
    parents.

    Si les settings pour tool.fixtup sont absents, ils sont écrits à la fin du fichier projet. Cette fonction est
    utilisé par la command `fixtup init` lors de l'initialisation d'un projet fixtup.

    En cas d'absence d'un fichier de configuration, un message d'erreur est affiché à l'utilisateur.
    :param settings:
    :return:
    """
    raise NotImplementedError()
