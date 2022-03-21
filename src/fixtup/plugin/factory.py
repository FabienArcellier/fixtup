from fixtup.factory import factory, RuntimeContext
from fixtup.plugin.base import PluginEngine
from fixtup.plugin.mock import MockPluginEngine
from fixtup.plugin.python import PythonPluginEngine


@factory
def lookup_plugin_engine(context: RuntimeContext) -> PluginEngine:

    if context.unittest:
        return MockPluginEngine()
    else:
        return PythonPluginEngine()
