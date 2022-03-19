from unittest.mock import Mock

from fixtup.factory import factory, RuntimeContext
from fixtup.fixture.base import FixtureEngine


@factory
def lookup_fixture_engine(context: RuntimeContext) -> FixtureEngine:
    """
    """
    from fixtup.fixture.base import FixtureEngine

    return FixtureEngine(Mock(), Mock())
