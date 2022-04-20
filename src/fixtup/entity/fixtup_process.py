from typing import List, Optional

import attr

from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.exceptions import FixtupException
from fixtup.lib.conditions import unique
from fixtup.lib.list import first

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
        _fixture = first(self.mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        assert _fixture is not None

        _fixture.started()

    def fixture_stopped(self, fixture: Fixture):
        _fixture = first(self.mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        assert _fixture is not None

        _fixture.stopped()

    def fixture_unmounted(self, fixture: Fixture):
        _fixture = first(self.mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        if _fixture is not None:
            _fixture.unmounted()
            self.mounted_fixtures.remove(_fixture)

        assert unique(self.mounted_fixtures, lambda f: f.identifier)

    def is_mounted(self, fixture_template: FixtureTemplate) -> bool:
        _fixture = first(self.mounted_fixtures, lambda f: f.template_identifier == fixture_template.identifier)
        return _fixture is not None

    def fixture(self, fixture_template: FixtureTemplate) -> Fixture:
        _fixture = first(self.mounted_fixtures, lambda f: f.template_identifier == fixture_template.identifier)
        if _fixture is None:
            raise FixtupException('no fixture is mounted for this fixture template, use is_mounted before invoking fixture()')

        return _fixture


"""
Cette entité a un scope d'application à l'échelle du process. Elle maintient la liste des fixtures
déjà montées.
"""
fixtup_process = FixtupProcess()
