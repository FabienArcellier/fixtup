from fixtup.entity.fixtup_process import fixtup_process, FixtupProcess
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

    # In automatic testing of fixtup itself, we need
    # to ensure the fixtup process is not shared for
    # some test.
    #
    # When the runtime context requires to emulate
    # a new test runtime process, we set a brand new
    # FixtupProcess
    if context.emulate_new_process:
        _fixtup_process = FixtupProcess()
    else:
        _fixtup_process = fixtup_process

    if context.unittest:
        return FixtureEngine(MockHookEngine(), plugin_engine, _fixtup_process)
    else:
        return FixtureEngine(PythonHookEngine(), plugin_engine, _fixtup_process)
