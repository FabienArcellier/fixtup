import typing
from typing import List

from fixtup.factory import factory, RuntimeContext

if typing.TYPE_CHECKING:
    from fixtup.settings.base import SettingsParser


@factory
def lookup_parsers(context: RuntimeContext) -> List['SettingsParser']:
    """
    When looking for a manifest, we first favor the setup.cfg file because the pyproject.toml file
    is generated by default. It is sometimes not used.

    If the manifest of setup.cfg is present, that means the project has choosen the way of setuptools
    recommand to package.
    """
    from fixtup.settings.module import ModuleSettings
    from fixtup.settings.setup_cfg import SetupCfg
    from fixtup.settings.pyproject_toml import PyprojectToml

    return [ModuleSettings(), SetupCfg(), PyprojectToml()]
