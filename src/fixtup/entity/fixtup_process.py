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
    mounted_fixtures: List[Fixture] = attr.ib(factory=list)

    def fixture_mounted(self, fixture: Fixture):
        self.mounted_fixtures.append(fixture)
        fixture.mounted()

        # Post-conditions
        assert unique(self.mounted_fixtures, lambda f: f.identifier)

    def fixture_started(self, fixture: Fixture):
        fixture = first(self.mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        assert fixture is not None

        fixture.started()

    def fixture_stopped(self, fixture: Fixture):
        fixture = first(self.mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        assert fixture is not None

        fixture.stopped()

    def fixture_unmounted(self, fixture: Fixture):
        fixture = first(self.mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        if fixture is not None:
            fixture.unmounted()

