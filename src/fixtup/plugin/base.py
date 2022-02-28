
class Plugin():

    def invoke(self, event: str, *args, **kwargs):
        raise NotImplementedError()

