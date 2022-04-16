import importlib
from types import ModuleType
from typing import List


import attr

from fixtup.exceptions import PluginRuntimeError
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
                try:
                    function(*args, **kwargs)
                except Exception as exception:
                    raise PluginRuntimeError(str(exception), plugin.__name__) from exception

    def register_plugin(self, module: str):
        logger = get_logger()
        try:
            plugin = importlib.import_module(module)
            self.plugins.append(plugin)
        except ModuleNotFoundError:
            logger.error(f'plugin "{module}" is missing, check if the module "{module}" is installed in your python venv')

