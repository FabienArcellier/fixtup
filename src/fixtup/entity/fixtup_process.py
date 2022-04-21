import copy
from typing import List, Optional, Tuple

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

    * a list of mounted fixtures - fixtures that has been mounted
    """
    _mounted_fixtures_detailled: List[Tuple[FixtureTemplate, Fixture]] = attr.ib(factory=list)
    _mounted_fixtures: List[Fixture] = attr.ib(factory=list)

    def fixture_mounted(self, template:FixtureTemplate ,fixture: Fixture):
        self._mounted_fixtures.append(fixture)
        self._mounted_fixtures_detailled.append((template, fixture))
        fixture.mounted()

        # Post-conditions
        assert unique(self._mounted_fixtures, lambda f: f.identifier)

    def fixture_started(self, fixture: Fixture):
        _fixture = first(self._mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        assert _fixture is not None

        _fixture.started()

    def fixture_stopped(self, fixture: Fixture):
        _fixture = first(self._mounted_fixtures, lambda f: f.identifier == fixture.identifier)
        assert _fixture is not None

        _fixture.stopped()

    def fixture_unmounted(self, fixture: Fixture):
        for index, (template, _fixture) in enumerate(copy.copy(self._mounted_fixtures_detailled)):
            if _fixture.identifier == fixture.identifier:
                _fixture.unmounted()
                del self._mounted_fixtures_detailled[index]
                del self._mounted_fixtures[index]

        assert unique(self._mounted_fixtures, lambda f: f.identifier)

    def is_mounted(self, fixture_template: FixtureTemplate) -> bool:
        _fixture = first(self._mounted_fixtures, lambda f: f.template_identifier == fixture_template.identifier)
        return _fixture is not None

    def fixture(self, fixture_template: FixtureTemplate) -> Fixture:
        _fixture = first(self._mounted_fixtures, lambda f: f.template_identifier == fixture_template.identifier)
        if _fixture is None:
            raise FixtupException('no fixture is mounted for this fixture template, use is_mounted before invoking fixture()')

        return _fixture

    def mounted_fixtures(self) -> List[Tuple[FixtureTemplate, Fixture]]:
        return copy.copy(self._mounted_fixtures_detailled)


"""
Cette entité a un scope d'application à l'échelle du process. Elle maintient la liste des fixtures
déjà montées.
"""
fixtup_process = FixtupProcess()
