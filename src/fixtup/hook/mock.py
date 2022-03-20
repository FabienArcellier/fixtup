from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.hook.base import HookEngine, HookEvent
from fixtup.logger import get_logger


class MockHookEngine(HookEngine):

    def run(self, event: HookEvent, template: FixtureTemplate) -> None:
        logger = get_logger()
        logger.debug(f"run mock for hook {event.value} in {template.identifier}")
