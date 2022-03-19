from enum import Enum
import os.path

import attr

from fixtup.entity.fixture_template import FixtureTemplate


class State(Enum):
    """
    This state means a directory for the fixture already exists
    and is ready to use
    """
    Reserved = "reserved"
    Mounted = "mounted"
    Started = "started"
    Stopped = "stopped"
    Unmounted = "unmounted"


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
            state=State.Reserved
        )

    def mounted(self):
        assert self.state == State.Reserved
        self.state = State.Mounted

    def started(self):
        assert self.state == State.Mounted or self.state == State.Stopped
        self.state = State.Started

    def stopped(self):
        assert self.state == State.Started
        self.state = State.Stopped

    def unmounted(self):
        assert self.state == State.Stopped or self.state == State.Mounted
        self.state = State.Unmounted
