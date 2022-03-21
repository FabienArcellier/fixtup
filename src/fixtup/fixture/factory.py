from fixtup.factory import factory, RuntimeContext
from fixtup.fixture.base import FixtureEngine
from fixtup.hook.mock import MockHookEngine
from fixtup.hook.python import PythonHookEngine
from fixtup.plugin.factory import lookup_plugin_engine


@factory
def lookup_fixture_engine(context: RuntimeContext) -> FixtureEngine:
    """
    """
    from fixtup.fixture.base import FixtureEngine

    plugin_engine = lookup_plugin_engine()
    if context.unittest:
        return FixtureEngine(MockHookEngine(), plugin_engine)
    else:
        return FixtureEngine(PythonHookEngine(), plugin_engine)
