import os.path
from typing import Optional, Dict, Any, List

import attr


@attr.s
class Settings:
    """

    """

    """
    The file of path that contains the configuration of fixtup
    """
    configuration_path: Optional[str] = attr.ib()

    """
    The path to the repository that contains the fixtures
    """
    fixtures: str = attr.ib()

    """
    list of python modules to load as fixtup plugin.

    The modules must be installed in the system or in the same virtual environment as
    fixup.

    If a module is not setup, fixtup displays a warning but continues its execution.
    """
    plugins: List[str] = attr.ib(factory=list)

    @classmethod
    def from_configuration(cls, settings: Dict[str, Any]) -> 'Settings':
        """
        load the settings from a simple dictionary with key value configure
        through `fixtup.configure`

        :param settings: key / value with settings specify by the user
        :return:
        """
        _settings: Dict[str, Any] = {'configuration_path': None}
        fields = [field for field in attr.fields(cls)]
        for key, value in settings.items():
            if key in fields:
                _settings[key] = value

        return Settings(**_settings)

    @classmethod
    def from_manifest(cls, manifest_path: str, settings: dict) -> 'Settings':
        """
        load settings entity based on a manifest lik pyproject.toml or setup.cfg

        the manifest is already parsed before being managed by this factory. The goal of this
        factory is to keep the information of origin of settings.

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

