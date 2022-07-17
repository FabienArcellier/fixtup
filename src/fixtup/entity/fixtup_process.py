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
    runtime. The process is usually the test runtime, so it can be unittest or pytest for example.

    The information will be :

    * a list of fixtures that are up
    """
    _active_fixtures_detailled: List[Tuple[FixtureTemplate, Fixture]] = attr.ib(factory=list)
    _up_fixtures: List[Fixture] = attr.ib(factory=list)

    def fixture_up(self, template: FixtureTemplate, fixture: Fixture):
        fixture.up()
        self._up_fixtures.append(fixture)
        self._active_fixtures_detailled.append((template, fixture))

        # check invariant, the same fixture must be registered only once as mounted.
        assert unique(self._up_fixtures, lambda f: f.identifier)

    def fixture_down(self, fixture: Fixture):
        _fixture = first(self._up_fixtures, lambda f: f.identifier == fixture.identifier)
        assert _fixture is not None

        for index, (template, _fixture) in enumerate(copy.copy(self._active_fixtures_detailled)):
            if _fixture.identifier == fixture.identifier:
                _fixture.down()
                del self._active_fixtures_detailled[index]
                del self._up_fixtures[index]

        # check invariant, the same fixture must be registered only once as mounted.
        assert unique(self._up_fixtures, lambda f: f.identifier)

    def is_up(self, fixture_template: FixtureTemplate) -> bool:
        _fixture = first(self._up_fixtures, lambda f: f.template_identifier == fixture_template.identifier)
        return _fixture is not None

    def fixture(self, fixture_template: FixtureTemplate) -> Fixture:
        """
        retrieve a running fixture for reuse instead of loading a new one.
        Usually these are the fixtures that have the `keep_up` policy active.

        :param fixture_template:
        """
        _fixture = first(self._up_fixtures, lambda f: f.template_identifier == fixture_template.identifier)
        if _fixture is None:
            raise FixtupException('no fixture is started for this fixture template, use is_started before invoking fixture()')

        return _fixture

    def active_fixtures(self) -> List[Tuple[FixtureTemplate, Fixture]]:
        return copy.copy(self._active_fixtures_detailled)


"""
This entity has a scope of application at the process level.
It maintains the list of fixtures already mounted.
"""
fixtup_process = FixtupProcess()
