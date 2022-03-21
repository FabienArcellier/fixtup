from fixtup.plugin.base import PluginEngine


class Mock(PluginEngine):

    def invoke(self, event: str, *args, **kwargs):
        """
        invoke the plugin based on an event

        :param args:
        :param kwargs:
        :return:
        """
        return
