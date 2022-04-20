from enum import Enum

from fixtup.entity.fixture_template import FixtureTemplate


class HookEvent(Enum):
    mounting = "mounting"
    starting = "starting"
    stopping = "stopping"
    unmounting = "unmounting"


class HookEngine:

    def run(self, event: HookEvent, template: FixtureTemplate) -> None:
        raise NotImplementedError
