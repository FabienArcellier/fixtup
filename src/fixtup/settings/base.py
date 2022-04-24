import os
from typing import Optional, List

from fixtup.entity.project_manifest import ProjectManifests
from fixtup.entity.settings import Settings
from fixtup.exceptions import PythonManifestMissing, FixtupSettingsMissing, FixtupSettingsAlreadyPresent
from fixtup.settings.factory import lookup_parsers

RESOURCE_DIR = os.path.realpath(os.path.join(__file__, '..', 'resource'))


class SettingsParser:

    """
    Le nom du fichier qui caractérise le manifest.
    """
    manifest: Optional[str] = None

    def has_manifest(self, path: str) -> bool:
        """
        check if the manifest exists in the current path
        """
        raise NotImplementedError

    def contains_settings(self, path: str) -> bool:
        raise NotImplementedError

    def read_settings(self, path: str) -> Settings:
        raise NotImplementedError

    def append_settings(self, settings: Settings) -> None:
        raise NotImplementedError


def list_project_manifests() -> ProjectManifests:
    """
    browses the current folder then the parent folders to identify the
    python manifests in which fixtup can register

    :return: a list of manifest identifier
    """

    manifests: List[str] = []
    starting_path = os.getcwd()
    parsers = lookup_parsers()
    path = starting_path
    is_python_project = False
    while is_python_project is False and os.path.dirname(path) != path:
        for parser in parsers:
            if parser.has_manifest(path):
                if parser.manifest is not None:
                    manifests.append(os.path.join(path, parser.manifest))

        path = os.path.dirname(path)

    project_manifests = ProjectManifests.create_from_path(manifests)

    if project_manifests.missing():
        raise PythonManifestMissing(
            "not a python project (or any of the parent directories): setup.cfg or pyproject.toml missing")

    return project_manifests


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
                    settings = parser.read_settings(path)
                    if not os.path.isdir(settings.fixtures_dir):
                        os.makedirs(settings.fixtures_dir)

                    return settings

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
    parsers = lookup_parsers()
    for parser in parsers:
        if settings.manifest_identifier == parser.manifest:
            if settings.configuration_dir is not None and parser.contains_settings(settings.configuration_dir):
                raise FixtupSettingsAlreadyPresent(f"fail to write settings because it already exists in {settings.manifest_path}")

            parser.append_settings(settings)
            return

    raise NotImplementedError(f"fail to append those settings")
