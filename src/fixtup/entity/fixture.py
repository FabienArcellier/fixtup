from enum import Enum
import os.path

import attr

from fixtup.entity.fixture_template import FixtureTemplate


class State(Enum):
    """
    This state means a directory for the fixture already exists
    and is ready to use

    :see: https://fixtup.readthedocs.io/en/latest/concepts.html#term-fixture-livecycle
    """
    Up = "up"
    Ready = "ready"
    Down = "down"


@attr.s
class Fixture:

    """
    the unique identifier that characterizes the fixture once mounted

    ex: simple_database_tr4vr5
    """
    identifier: str = attr.ib()
    directory: str = attr.ib()
    state: State = attr.ib()
    template_identifier: str = attr.ib()

    @classmethod
    def create_from_template(cls, fixture_template: FixtureTemplate, fixture_path: str) -> 'Fixture':
        identifier = os.path.basename(fixture_path)
        return Fixture(
            identifier=identifier,
            directory=fixture_path,
            template_identifier=fixture_template.identifier,
            state=State.Down
        )

    @classmethod
    def fake(cls, **kwargs) -> 'Fixture':
        """
        Return a fake entity that is usable for automated testing.

        Any args may be override
        """
        return Fixture(
            identifier=kwargs.get('identifier', 'fixture_1234'),
            directory=kwargs.get('directory', '/tmp/fixture_1234'),
            template_identifier=kwargs.get('template_identifier', 'fixture'),
            state=kwargs.get('state', State.Down),
        )

    def setup_data(self):
        assert self.state == State.Up
        self.state = State.Ready

    def teardown_data(self):
        assert self.state == State.Ready
        self.state = State.Up

    def up(self):
        assert self.state == State.Down
        self.state = State.Up

    def down(self):
        assert self.state == State.Up
        self.state = State.Down
