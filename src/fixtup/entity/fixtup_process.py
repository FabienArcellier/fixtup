from typing import List

import attr

from fixtup.entity.fixture import Fixture
from fixtup.lib.conditions import unique
from fixtup.lib.lib import first


@attr.s
class FixtupProcess:
    """
    Saves informations about fixtup relative to the current process
    runtime. The process may be unittest or pytest.

    The information will be :

    * a list of active fixtures - fixtures that has been mounted
    """
    active_fixtures: List[Fixture] = attr.ib(factory=dict)

    def mounted(self, fixture: Fixture):
        self.active_fixtures.append(fixture)

        # Post-conditions
        assert unique(self.active_fixtures, lambda f: f.identifier)

    def started(self, fixture: Fixture):
        active_fixture = first(self.active_fixtures, lambda f: f.identifier == fixture.identifier)
