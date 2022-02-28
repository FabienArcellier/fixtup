"""

"""

"""
On this event, a plugin can enrich the fixture record
with specific requirement ask to the user through a prompt

For example, it may ask the user if he want to generate a docker-compose.yml
template.

>>> def ask_user_input(fixture: Fixture, *args, **kwargs):
>>>     prompt = lookup_prompt()
>>>     prompt.confirm("Is this fixture use docker container ? ")
>>>
>>> plugin.on(event.BEFORE_SCAFFOLD_NEW_FIXTURE, ask_user_input)
"""
BEFORE_SCAFFOLD_NEW_FIXTURE = "BEFORE_SCAFFOLD_NEW_FIXTURE"

"""
On this event, a plugin can write artefacts in a fixture that just have been
generated.
That's here the plugin will write the docker-compose.yml if the user answer
on the prompt he needs one.

>>>
>>>
"""
SCAFFOLD_NEW_FIXTURE = "SCAFFOLD_NEW_FIXTURE"
