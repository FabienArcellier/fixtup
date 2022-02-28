import os

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.validation import Document, Validator, ValidationError

from fixtup.prompt.base import Prompt


class PromptToolkit(Prompt):

    def new_fixture(self, fixture_repository: str) -> str:
        fixture = prompt('Fixture identifier ? ',
                         completer=directory_completer(fixture_repository),
                         validator=NewFixtureValidator(fixture_repository))

        return fixture


    def confirm(self, question: str) -> bool:
        return confirm(question)


class NewFixtureValidator(Validator):
    """
    Check if the identifier of the fixture given by the user is valid

    * it must not exists in the fixture repository
    * it must be in the current directory, not in a subdirectory
    """

    def __init__(self, fixture_repository: str):
        super().__init__()
        self.fixture_repository = fixture_repository

    def validate(self, document: Document):
        text = document.text

        if os.path.isdir(os.path.join(self.fixture_repository, text)):
            raise ValidationError(message=f'fixture "{text}" already exists')

        if os.path.sep in text:
            raise ValidationError(message=f'fixture "{text}" can not be in a subdirectory')


def directory_completer(directory) -> FuzzyWordCompleter:
    """
    return a list of element on which perform autocomplete based
    on directory content

    >>> directory_completer('/home/hello')
    :param directory: the directory to scan to get the autocomplete proposition
    """
    elements = sorted(os.listdir(directory))
    return FuzzyWordCompleter(elements)
