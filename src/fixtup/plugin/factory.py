from fixtup.factory import RuntimeContext, factory


@factory
def lookup_plugin(context: RuntimeContext):
    from fixtup.plugin.mock import Mock
    return Mock()
