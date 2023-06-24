from fixtup import ctx
from fixtup.entity.fixtup import Driver
from fixtup.prompt import Prompt


def lookup_prompt() -> Prompt:
    """
    """
    fixtup_context = ctx.get()
    driver_prompt = fixtup_context.driver_prompt

    if driver_prompt == Driver.prompt_toolkit:
        from fixtup.prompt.prompt_toolkit import PromptToolkit
        return PromptToolkit()
    elif driver_prompt == Driver.mock:
        from fixtup.prompt.mock import Mock
        return Mock()
    else:
        raise NotImplementedError(f"{fixtup_context.driver_prompt} is not supported")
