from typing import Optional

from fixtup.entity.fixtup_process import fixtup_process, FixtupProcess
from fixtup.factory import factory, RuntimeContext
from fixtup.fixture.base import FixtureEngine
from fixtup.hook.mock import MockHookEngine
from fixtup.hook.python import PythonHookEngine
from fixtup.plugin.factory import lookup_plugin_engine

fixture_engine: Optional[FixtureEngine] = None


@factory
def lookup_fixture_engine(context: RuntimeContext) -> FixtureEngine:
    """
    """
    global fixture_engine
    if fixture_engine is not None and not context.emulate_new_process:
        return fixture_engine
    elif fixture_engine is not None and context.emulate_new_process:
        fixture_engine.unregister_process_teardown()
        fixture_engine.process_teardown_exit()
        fixture_engine = None

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
        fixture_engine = FixtureEngine(MockHookEngine(), plugin_engine, _fixtup_process)
    else:
        fixture_engine = FixtureEngine(PythonHookEngine(), plugin_engine, _fixtup_process)

    return fixture_engine
