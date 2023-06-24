from typing import Optional

from fixtup import ctx
from fixtup.entity.fixtup_process import fixtup_process, FixtupProcess
from fixtup.fixture.base import FixtureEngine
from fixtup.hook.factory import lookup_hook_engine
from fixtup.plugin.factory import lookup_plugin_engine

fixture_engine: Optional[FixtureEngine] = None


def lookup_fixture_engine(highest_context: bool = False) -> FixtureEngine:
    fixtup_context = ctx.get()
    global fixture_engine
    if fixture_engine is not None and highest_context is False:
        return fixture_engine
    if fixture_engine is not None and not fixtup_context.emulate_new_process:
        return fixture_engine
    elif fixture_engine is not None and fixtup_context.emulate_new_process:
        fixture_engine.unregister_process_teardown()
        fixture_engine.process_teardown_exit()
        fixture_engine = None

    plugin_engine = lookup_plugin_engine()
    hook_engine = lookup_hook_engine()

    # In automatic testing of fixtup itself, we need to ensure the fixtup process is not shared for
    # some test.
    #
    # When the runtime context requires to emulate a new test runtime process, we set a brand new
    # FixtupProcess
    if fixtup_context.emulate_new_process:
        _fixtup_process = FixtupProcess()
    else:
        _fixtup_process = fixtup_process

    fixture_engine = FixtureEngine(hook_engine, plugin_engine, _fixtup_process)
    return fixture_engine

def reset_fixture_engine() -> None:
    global fixture_engine
    fixture_engine = None
