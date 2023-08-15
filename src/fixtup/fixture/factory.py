from fixtup.context import lib_context
from fixtup.entity.fixtup_process import fixtup_process, FixtupProcess
from fixtup.fixture.base import FixtureEngine
from fixtup.hook.factory import lookup_hook_engine
from fixtup.plugin.factory import lookup_plugin_engine


def lookup_fixture_engine(highest_context: bool = False) -> FixtureEngine:
    fixtup_context = lib_context()
    if fixtup_context.engine is not None and highest_context is False:
        return fixtup_context.engine
    if fixtup_context.engine is not None and not fixtup_context.emulate_new_process:
        return fixtup_context.engine
    elif fixtup_context.engine is not None and fixtup_context.emulate_new_process:
        fixtup_context.engine.unregister_process_teardown()
        fixtup_context.engine.process_teardown_exit()
        fixtup_context.engine = None

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

def fixture_engine_down() -> None:
    global fixture_engine
    fixture_engine = None
