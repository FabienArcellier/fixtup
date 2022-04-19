import copy
import os.path
from typing import Optional, Dict, Any, List

import attr

from fixtup.entity.project_manifest import ProjectManifest


@attr.s
class Settings:
    """

    """

    """
    The file of path that contains the configuration of fixtup
    """
    manifest: Optional[ProjectManifest] = attr.ib()

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

        >>> settings_def = {
        >>>    "fixtures": os.path.join(SCRIPT_DIR, "../fixtures/fixtup"),
        >>>    'plugins': [
        >>>        'fixtup.plugins.dummy_plugin_error'
        >>>    ]
        >>> }
        >>> settings = Settings.from_configuration(settings)

        :param settings: key / value with settings specify by the user
        :return:
        """
        _settings: Dict[str, Any] = {'manifest': None}
        fields = [field.name for field in attr.fields(cls)]
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

        _settings: Dict[str, Any] = {'manifest': ProjectManifest.create_from_path(manifest_path)}
        fields = [field.name for field in attr.fields(cls)]
        for key, value in settings.items():
            if key in fields:
                _settings[key] = value

        return Settings(**_settings)

    @classmethod
    def default_settings_for_init(cls, manifest: ProjectManifest, fixture_repository: str) -> 'Settings':
        """
        create default settings to write as fixtup configuration when a user
        initialize its python project with the command ``fixtup init``

        >>> from fixtup.settings.base import write_settings
        >>>
        >>> project_manifest = ProjectManifest.create_from_path("/home/xxx/my_project/setup.cfg")
        >>> settings = Settings.default_settings_for_init(project_manifest, "tests/fixtures")
        >>> write_settings(settings)

        :param settings: key / value with settings extract from manifest
        """
        return Settings(
            manifest=copy.deepcopy(manifest),
            fixtures=fixture_repository,
            plugins=[
                "fixtup.plugins.dotenv",
                "fixtup.plugins.docker"
            ]
        )

    @property
    def configuration_dir(self) -> Optional[str]:
        if self.manifest is None:
            return None

        return os.path.dirname(self.manifest.path)

    @property
    def manifest_path(self) -> Optional[str]:
        if self.manifest is not None:
            return self.manifest.path

        return None

    @property
    def manifest_identifier(self) -> Optional[str]:
        if self.manifest is not None:
            return self.manifest.identifier

        return None

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

