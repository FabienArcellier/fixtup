from enum import Enum

class PluginEvent(Enum):
    fixture_generated = "generated_fixture"
    mounted = "mounted"
    started = "started"
    stopped = "stopped"
    unmounted = "unmounted"


class PluginEngine:

    def run(self, event: PluginEvent, *args, **kwargs):
        raise NotImplementedError()

    def register_plugin(self, module: str):
        raise NotImplementedError()


def event_to_function(event: PluginEvent) -> str:
    _event_to_function = {
        event.fixture_generated: "on_mounting",
        event.mounted: "on_mounting",
        event.started: "on_mounting",
        event.stopped: "on_mounting",
        event.unmounted: "on_mounting",
    }

    return _event_to_function[event]  # type: ignore
