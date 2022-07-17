from enum import Enum
from types import ModuleType

import attr


class PluginEvent(Enum):
    new_fixture = "new_fixture"
    setup_data = "setup_data"
    starting = "starting"
    stopping = "stopping"
    teardown_data = "teardown_data"


@attr.s
class Plugin:
    module_name: str = attr.ib()
    module: ModuleType = attr.ib()

    @classmethod
    def create_from_module(cls, module: ModuleType):
        return Plugin(
            module_name=module.__name__,
            module=module
        )
