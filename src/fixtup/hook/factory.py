from fixtup.context import lib_context
from fixtup.hook.base import HookEngine
from fixtup.hook.mock import MockHookEngine
from fixtup.hook.python import PythonHookEngine


def lookup_hook_engine() -> HookEngine:
    fixtup_context = lib_context()
    hook_engine: HookEngine
    if fixtup_context.enable_hooks is True:
        hook_engine = PythonHookEngine()
    else:
        hook_engine = MockHookEngine()

    return hook_engine
