from fixtup.factory import factory, RuntimeContext
from fixtup.hook.base import HookEngine
from fixtup.hook.mock import MockHookEngine
from fixtup.hook.python import PythonHookEngine
from fixtup.plugin.base import PluginEngine


@factory
def lookup_hook_engine(context: RuntimeContext) -> HookEngine:
    hook_engine: HookEngine
    if context.enable_hooks:
        hook_engine = PythonHookEngine()
    else:
        hook_engine = MockHookEngine()


    return hook_engine
