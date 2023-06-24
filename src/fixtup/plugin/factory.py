from fixtup import ctx
from fixtup.plugin.base import PluginEngine
from fixtup.plugin.mock import MockPluginEngine
from fixtup.plugin.python import PythonPluginEngine
from fixtup.settings import read_settings


def lookup_plugin_engine() -> PluginEngine:
    fixtup_context = ctx.get()
    plugin_engine: PluginEngine
    if fixtup_context.enable_plugins is True:
        plugin_engine = PythonPluginEngine()
    else:
        plugin_engine = MockPluginEngine()

    settings = read_settings()
    for plugin in settings.plugins:
        plugin_engine.register_plugin(plugin)

    return plugin_engine
