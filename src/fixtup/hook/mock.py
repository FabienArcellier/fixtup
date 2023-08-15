from fixtup import logger
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.hook.base import HookEngine, HookEvent


class MockHookEngine(HookEngine):

    def run(self, event: HookEvent, template: FixtureTemplate) -> None:
        logger.debug(f"run mock for hook {event.value} in {template.identifier}")
