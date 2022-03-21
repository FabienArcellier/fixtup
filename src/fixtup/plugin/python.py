import importlib
from types import ModuleType
from typing import List


import attr

from fixtup.entity.fixture import Fixture
from fixtup.logger import get_logger
from fixtup.plugin.base import PluginEngine, PluginEvent


@attr.s
class PythonPluginEngine(PluginEngine):
    plugins: List[ModuleType] = attr.ib(factory=list)

    def run(self, event: PluginEvent, *args, **kwargs):
        pass

    def register_plugin(self, module: str):
        logger = get_logger()
        try:
            plugin = importlib.import_module(module)
            self.plugins.append(plugin)
        except ModuleNotFoundError:
            logger.error(f'plugin "{module}" is missing, check if the module "{module}" is installed in your python venv')

