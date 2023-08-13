from fixtup.context import lib_context
from fixtup.plugin.base import PluginEngine
from fixtup.plugin.mock import MockPluginEngine
from fixtup.plugin.python import PythonPluginEngine


def lookup_plugin_engine() -> PluginEngine:
    fixtup_context = lib_context()
    plugin_engine: PluginEngine
    if fixtup_context.enable_plugins is True:
        plugin_engine = PythonPluginEngine()
    else:
        plugin_engine = MockPluginEngine()

    # settings = read_settings()
    for plugin in fixtup_context.plugins:
        plugin_engine.register_plugin(plugin)

    return plugin_engine
