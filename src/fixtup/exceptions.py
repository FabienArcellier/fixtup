from fixtup.entity.plugin import Plugin


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
