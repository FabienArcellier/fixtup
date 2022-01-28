import os
from typing import Optional, Dict, Any

import attr

@attr.s
class Settings:
    manifest_dir: Optional[str] = attr.ib()
    fixtures: str = attr.ib()

    @classmethod
    def from_configuration(cls, settings: Dict[str, Any]) -> 'Settings':
        """
        load the settings from a simple dictionary with key value configure
        through `fixtup.configure`

        :param settings: key / value with settings specify by the user
        :return:
        """
        _settings: Dict[str, Any] = {'manifest_dir': None}
        fields = [field.name for field in attr.fields(cls)]
        for key, value in settings.items():
            if key in fields:
                _settings[key] = value

        return Settings(**_settings)

    @classmethod
    def from_manifest(cls, manifest_dir: str, settings: dict) -> 'Settings':
        """

        :param manifest_dir: the directory that contains the manifest of python project
        :param settings: key / value with settings extract from manifest
        """

        _settings = {'manifest_dir': manifest_dir}
        fields = [field.name for field in attr.fields(cls)]
        for key, value in settings.items():
            if key in fields:
                _settings[key] = value

        return Settings(**_settings)

    @property
    def fixtures_dir(self):
        """
        return the path of the directory that contains the fixtures.
        The path is an absolute path.

        :return: absolute path of the directory that contains the fixtures
        """
        if self.manifest_dir is None:
            return self.fixtures
        else:
            return os.path.join(self.manifest_dir, self.fixtures)

