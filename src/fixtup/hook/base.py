from enum import Enum

from fixtup.entity.fixture_template import FixtureTemplate


class HookEvent(Enum):
    mounted="mounted"
    started="started"
    stopped="stopped"
    unmounted="unmounted"


class HookEngine:

    def run(self, event: HookEvent, template: FixtureTemplate) -> None:
        raise NotImplementedError
