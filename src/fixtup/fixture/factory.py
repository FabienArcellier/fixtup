from unittest.mock import Mock

from fixtup.factory import factory, RuntimeContext
from fixtup.fixture.base import FixtureEngine
from fixtup.hook.mock import MockHookEngine
from fixtup.hook.python import PythonHookEngine


@factory
def lookup_fixture_engine(context: RuntimeContext) -> FixtureEngine:
    """
    """
    from fixtup.fixture.base import FixtureEngine

    if context.unittest:
        return FixtureEngine(MockHookEngine(), Mock())
    else:
        return FixtureEngine(PythonHookEngine(), Mock())
