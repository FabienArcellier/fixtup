import importlib
from types import ModuleType
from typing import List


import attr

from fixtup.logger import get_logger
from fixtup.plugin.base import PluginEngine, PluginEvent, event_to_function


@attr.s
class PythonPluginEngine(PluginEngine):
    plugins: List[ModuleType] = attr.ib(factory=list)

    def run(self, event: PluginEvent, *args, **kwargs):
        function_name = event_to_function(event)
        for plugin in self.plugins:
            function = getattr(plugin, function_name, None)
            if function is not None:
                function(*args, **kwargs)

    def register_plugin(self, module: str):
        logger = get_logger()
        try:
            plugin = importlib.import_module(module)
            self.plugins.append(plugin)
        except ModuleNotFoundError:
            logger.error(f'plugin "{module}" is missing, check if the module "{module}" is installed in your python venv')

