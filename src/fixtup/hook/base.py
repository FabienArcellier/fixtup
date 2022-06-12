from enum import Enum

from fixtup.entity.fixture_template import FixtureTemplate


class HookEvent(Enum):
    mounting = "mounting"
    setup_data = "setup_data"
    starting = "starting"
    stopping = "stopping"
    teardown_data = "teardown_data"
    unmounting = "unmounting"


class HookEngine:

    def run(self, event: HookEvent, template: FixtureTemplate) -> None:
        raise NotImplementedError
