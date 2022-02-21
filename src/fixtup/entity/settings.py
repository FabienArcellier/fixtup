import os.path
from typing import Optional, Dict, Any

import attr

@attr.s
class Settings:
    """
    The file of path that contains the configuration of fixtup
    """
    configuration_path: Optional[str] = attr.ib()

    """
    Le chemin du dossier qui contient les fixtures
    """
    fixtures: str = attr.ib()

    @classmethod
    def from_configuration(cls, settings: Dict[str, Any]) -> 'Settings':
        """
        load the settings from a simple dictionary with key value configure
        through `fixtup.configure`

        :param settings: key / value with settings specify by the user
        :return:
        """
        _settings: Dict[str, Any] = {'configuration_path': None}
        fields = [field.name for field in attr.fields(cls)]
        for key, value in settings.items():
            if key in fields:
                _settings[key] = value

        return Settings(**_settings)

    @classmethod
    def from_manifest(cls, manifest_path: str, settings: dict) -> 'Settings':
        """

        :param manifest_path: the path of the manifest that describes the python project (pyproject.toml, ...)
        :param settings: key / value with settings extract from manifest
        """

        _settings = {'configuration_path': manifest_path}
        fields = [field.name for field in attr.fields(cls)]
        for key, value in settings.items():
            if key in fields:
                _settings[key] = value

        return Settings(**_settings)

    @property
    def configuration_dir(self) -> Optional[str]:
        if self.configuration_path is None:
            return None

        return os.path.dirname(self.configuration_path)

    @property
    def fixtures_dir(self):
        """
        return the path of the directory that contains the fixtures.
        The path is an absolute path.

        :return: absolute path of the directory that contains the fixtures
        """
        if self.configuration_dir is None:
            return self.fixtures
        else:
            return os.path.join(self.configuration_dir, self.fixtures)

