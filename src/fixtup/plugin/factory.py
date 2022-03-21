from fixtup.factory import factory, RuntimeContext
from fixtup.plugin.base import PluginEngine
from fixtup.plugin.mock import MockPluginEngine
from fixtup.plugin.python import PythonPluginEngine
from fixtup.settings import read_settings


@factory
def lookup_plugin_engine(context: RuntimeContext) -> PluginEngine:
    plugin_engine: PluginEngine
    if context.unittest:
        plugin_engine = MockPluginEngine()
    else:
        plugin_engine = PythonPluginEngine()

    settings = read_settings()
    for plugin in settings.plugins:
        plugin_engine.register_plugin(plugin)

    return plugin_engine
