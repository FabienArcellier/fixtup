from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.entity.plugin import Plugin
from fixtup.hook.base import HookEvent


class FixtupException(Exception):

    def __init__(self, msg: str):
        """
        the attribute msg contains the message to display to the user.
        """
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return str(self.msg)


class PythonManifestMissing(FixtupException):
    pass


class FixtupSettingsMissing(FixtupException):
    pass


class FixtupSettingsAlreadyPresent(FixtupException):
    pass


class FixtureNotFound(FixtupException):
    pass


class PluginRuntimeError(FixtupException):

    def __init__(self, msg: str, plugin: Plugin):
        msg = f'{msg} - plugin: {plugin.module_name}'
        super().__init__(msg)


class HookRuntimeError(FixtupException):

    def __init__(self, msg: str, template: FixtureTemplate,hook_event: HookEvent, hook_script: str):
        msg = f'{msg} - fixture: {template.identifier}, hook: {hook_event}, hook_script: {hook_script}'
        super().__init__(msg)
