from fixtup.entity.plugin import PluginEvent
from fixtup.logger import get_logger


class PluginEngine:

    def run(self, event: PluginEvent, *args, **kwargs) -> None:
        raise NotImplementedError()

    def register_plugin(self, module: str) -> None:
        raise NotImplementedError()

    def release(self, event: PluginEvent, *args, **kwargs) -> None:
        """
        This method try to release resource instanciate through a plugin. We run the event
         in degraded mode. If it raise an error, it will ignore it.
        """
        logger = get_logger()
        logger.warning(f"release plugin resource due to internal error with event {event}")
        try:
            self.run(event, *args, **kwargs)
        except:
            pass


def event_to_function(event: PluginEvent) -> str:
    _event_to_function = {
        event.new_fixture: "on_new_fixture",
        event.starting: "on_starting",
        event.setup_data: "on_setup_data",
        event.stopping: "on_stopping",
        event.teardown_data: "on_teardown_data",
    }

    return _event_to_function[event]  # type: ignore
