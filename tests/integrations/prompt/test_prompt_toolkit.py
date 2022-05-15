import os
import unittest
from unittest.mock import Mock

from prompt_toolkit.validation import ValidationError

import fixtup
from fixtup.prompt.prompt_toolkit import NewFixtureValidator, directory_completer, \
    FixtureRepositoryValidator, RecursiveDirectoryCompleter, ChoicesValidator, PromptToolkit

class TestValidationError(unittest.TestCase):

    def test_ChoicesValidator_validate_should_accept_one_of_the_proposed_choice(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            validator = ChoicesValidator(['choice 1', 'choice 2'])
            document = Mock()
            document.text = 'choice 1'

            # Acts
            validator.validate(document=document)

    def test_ChoicesValidator_validate_should_accept_only_proposed_choices(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            validator = ChoicesValidator(['choice 1', 'choice 2'])
            document = Mock()
            document.text = 'choice'

            # Acts
            try:
                validator.validate(document=document)
                self.fail('the document is not a choice, this test should raise a ValidationError')
            except ValidationError as exception:
                pass

    def test_FixtureRepositoryValidator_validate_should_raise_validation_error_when_directory_exists_and_is_not_empty(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            validator = FixtureRepositoryValidator(os.getcwd())
            document = Mock()
            document.text = 'fixtup'

            # Acts
            try:
                validator.validate(document=document)
                self.fail('fixtup already contains files, validate should raise an error')
            except ValidationError as exception:
                pass

    def test_FixtureRepositoryValidator_validate_should_accept_directory_that_not_exists(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            validator = FixtureRepositoryValidator(os.getcwd())
            document = Mock()
            document.text = 'new_fixtup'

            # Acts
            validator.validate(document=document)

    def test_FixtureRepositoryValidator_validate_should_accept_empty_directory(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            # we have to create an empty directory because I can't save it
            # as git directory
            os.makedirs(os.path.join(os.getcwd(), 'new_fixtup'))

            validator = FixtureRepositoryValidator(os.getcwd())
            document = Mock()
            document.text = 'new_fixtup'

            # Acts
            validator.validate(document=document)

    def test_NewFixtureValidator_validate_should_raise_validation_error_when_fixture_already_exists(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), 'fixtup')
            validator = NewFixtureValidator(fixture_repository)
            document = Mock()
            document.text = 'hello'

            # Acts
            try:
                validator.validate(document=document)
                self.fail('hello fixture already exists, validate should raise an error')
            except ValidationError as exception:
                pass

    def test_NewFixtureValidator_validate_should_raise_validation_error_when_fixture_identifier_contains_path_split(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), 'fixtup')
            validator = NewFixtureValidator(fixture_repository)
            document = Mock()
            document.text = f'hello{os.path.sep}world'

            # Acts
            try:
                validator.validate(document=document)
                self.fail(f'hello{os.path.sep}world fixture is not valid')
            except ValidationError as exception:
                pass


class TestCompleter(unittest.TestCase):

    def test_directory_completer_should_expose_directory_in_autocomplete(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), 'fixtup')

            # Acts
            completer = directory_completer(fixture_repository)

            # Assert
            self.assertEqual(['hello', 'running', 'shared'], completer.words)

    def test_recursive_directory_completer_should_expose_all_subdirectories(self):
        # Arrange
        with fixtup.up('project_with_hidden_venv'):
            cwd = os.getcwd()

            # Acts
            completer = RecursiveDirectoryCompleter(cwd, ignore_hidden_directory=False)
            document = Mock()
            document.text = "tests/"
            completions = list(completer.get_completions(document, Mock()))

            # Assert
            self.assertEqual(2, len(completions))
            autocomplete = [completion.text for completion in completions]

            self.assertIn('.dist', autocomplete)
            self.assertIn('units', autocomplete)

    def test_recursive_directory_completer_should_expose_all_subdirectories_except_hidden(self):
        # Arrange
        with fixtup.up('project_with_hidden_venv'):
            cwd = os.getcwd()

            # Acts
            completer = RecursiveDirectoryCompleter(cwd)
            document = Mock()
            document.text = "tests/"
            completions = list(completer.get_completions(document, Mock()))

            # Assert
            self.assertEqual(1, len(completions))
            self.assertEqual('units', completions[0].text)


if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
