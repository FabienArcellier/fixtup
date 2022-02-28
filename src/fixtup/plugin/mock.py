from fixtup.plugin.base import Plugin


class Mock(Plugin):

    def invoke(self, event: str, *args, **kwargs):
        """
        invoke the plugin based on an event

        :param args:
        :param kwargs:
        :return:
        """
        return
