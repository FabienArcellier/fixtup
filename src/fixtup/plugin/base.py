from enum import Enum


class PluginEvent(Enum):
    generated_fixture="generated_fixture"
    mounted="mounted"
    started="started"
    stopped="stopped"
    unmounted="unmounted"


class PluginEngine():

    def run(self, event: str, *args, **kwargs):
        raise NotImplementedError()

