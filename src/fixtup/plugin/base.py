from enum import Enum

class PluginEvent(Enum):
    new_fixture = "new_fixture"
    mounting = "mounting"
    starting = "starting"
    stopping = "stopping"
    unmounting = "unmounting"


class PluginEngine:

    def run(self, event: PluginEvent, *args, **kwargs):
        raise NotImplementedError()

    def register_plugin(self, module: str):
        raise NotImplementedError()


def event_to_function(event: PluginEvent) -> str:
    _event_to_function = {
        event.new_fixture: "on_new_fixture",
        event.mounting: "on_mounting",
        event.starting: "on_starting",
        event.stopping: "on_stopping",
        event.unmounting: "on_unmounting",
    }

    return _event_to_function[event]  # type: ignore
