import os
from typing import List, Optional

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.validation import Document, Validator, ValidationError
from prompt_toolkit.completion import Completer, Completion, CompleteEvent

from fixtup.prompt.base import Prompt


class PromptToolkit(Prompt):

    def choice(self, question: str, choices: List[str], default: Optional[str] = None) -> str:
        if default is None:
            default = choices[0] if len(choices) > 0 else ""

        raw_choice = prompt(question + f" ({'/'.join(choices)}) [{default}] ",
                        completer=choices_completer(choices),
                        validator=ChoicesValidator(choices)),

        if raw_choice[0] == "":
            return default

        return raw_choice[0]

    def fixture_repository(self) -> str:
        cwd = os.getcwd()
        fixture_repository = prompt('Choose a directory to store fixture templates : ',
                         completer=RecursiveDirectoryCompleter(cwd),
                         validator=FixtureRepositoryValidator(cwd))

        return fixture_repository

    def new_fixture(self, fixture_repository: str) -> str:
        fixture = prompt('Choose a fixture identifier : ',
                         completer=directory_completer(fixture_repository),
                         validator=NewFixtureValidator(fixture_repository))

        return fixture

    def confirm(self, question: str, default: Optional[bool] = None) -> bool:
        default_value = None
        if default is not None:
            default_value = 'y' if default is True else 'n'

        return self.choice(question, choices=['y', 'n'], default=default_value) == 'y'


class ChoicesValidator(Validator):
    """
    The user has to pick of the proposed choices
    """

    def __init__(self, choices: List[str]):
        """

        :param cwd: current working directory
        """
        super().__init__()
        self.choices = choices

    def validate(self, document: Document):
        text = document.text

        if document.text != "" and document.text not in self.choices:
            raise ValidationError(message=f'you have to pick one of those choices: {self.choices}')

class FixtureRepositoryValidator(Validator):
    """
    Check if the choice of the directory choosen as fixture repository does not exists or
    is empty.

    Fixtup can't use a directory that exists and contains other file
    """

    def __init__(self, cwd: str):
        """

        :param cwd: current working directory
        """
        super().__init__()
        self.cwd = cwd

    def validate(self, document: Document):
        text = document.text

        target = os.path.join(self.cwd, text)
        if os.path.isdir(target) and len(os.listdir(target)) > 0:
            raise ValidationError(message=f'"{text}" must be a new directory or an empty directory.')


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


def choices_completer(choices: List[str]) -> FuzzyWordCompleter:
    """
    return a list of element on which perform autocomplete based
    on available choice.

    >>> choices_completer(['choice 1', 'choice 2'])
    """
    return FuzzyWordCompleter(choices)


def directory_completer(directory: str) -> FuzzyWordCompleter:
    """
    return a list of element on which perform autocomplete based
    on directory content. This method perform autocomplete only on
    the direct content of the directory

    >>> directory_completer('/home/hello')
    :param directory: the directory to scan to get the autocomplete proposition
    """
    elements = sorted(os.listdir(directory))
    return FuzzyWordCompleter(elements)


class RecursiveDirectoryCompleter(Completer):
    """
    provide autocompletion from a home folder and descend
    in the tree structure as the user enriches the path.

    * /home/hello/ will propose mydir1, dir2, dir3
    * /home/hello/myd will propose mydir1
    * /home/hello/mydir1/h will propose hive, headers

    >>> RecursiveDirectoryCompleter('/home/hello')

    :param directory: the folder on which to start the autocompletion
    :param ignore_hidden_directory: ignore the hidden directory when crawling
    """

    def __init__(self, directory: str, ignore_hidden_directory=True):
        super().__init__()
        self.directory = directory
        self.ignore_hidden_directory = ignore_hidden_directory

    def get_completions(self, document: Document, complete_event: CompleteEvent):
        base_directory = os.path.dirname(document.text)
        directory_to_autocomplete = os.path.basename(document.text)
        root_directory = os.path.join(self.directory, base_directory)

        if os.path.isdir(root_directory):
            for directory in os.listdir(root_directory):
                _complete_path = os.path.join(root_directory, directory)
                if not os.path.isdir(_complete_path):
                    continue

                if self.ignore_hidden_directory is True and directory.startswith('.'):
                    continue

                if directory_to_autocomplete in directory:
                    yield Completion(directory, start_position=-len(directory_to_autocomplete))
