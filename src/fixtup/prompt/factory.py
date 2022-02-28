from fixtup.factory import factory, RuntimeContext
from fixtup.prompt import Prompt


@factory
def lookup_prompt(context: RuntimeContext) -> Prompt:
    """
    """
    from fixtup.prompt.prompt_toolkit import PromptToolkit
    from fixtup.prompt.mock import Mock

    if context.unittest:
        return Mock()
    else:
        return PromptToolkit()
