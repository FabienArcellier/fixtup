from typing import List

import attr

from fixtup.entity.fixture import Fixture
from fixtup.lib.conditions import unique
from fixtup.lib.list import first
from fixtup.logger import get_logger


@attr.s
class FixtupProcess:
    """
    Saves informations about fixtup relative to the current process
    runtime. The process may be unittest or pytest.

    The information will be :

    * a list of active fixtures - fixtures that has been mounted
    """
    active_fixtures: List[Fixture] = attr.ib(factory=list)

    def fixture_mounted(self, fixture: Fixture):
        self.active_fixtures.append(fixture)
        fixture.mounted()

        # Post-conditions
        assert unique(self.active_fixtures, lambda f: f.identifier)

    def fixture_started(self, fixture: Fixture):
        active_fixture = first(self.active_fixtures, lambda f: f.identifier == fixture.identifier)
        assert active_fixture is not None

        active_fixture.started()

    def fixture_stopped(self, fixture: Fixture):
        active_fixture = first(self.active_fixtures, lambda f: f.identifier == fixture.identifier)
        assert active_fixture is not None

        active_fixture.stopped()

    def fixture_unmounted(self, fixture: Fixture):
        active_fixture = first(self.active_fixtures, lambda f: f.identifier == fixture.identifier)
        if active_fixture is not None:
            active_fixture.unmounted()

