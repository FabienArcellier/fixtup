import os
import unittest
from unittest.mock import Mock

from prompt_toolkit.validation import ValidationError

import fixtup
from fixtup.prompt.prompt_toolkit import NewFixtureValidator, directory_completer


class TestValidationError(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_should_raise_validation_error_when_fixture_already_exists(self):
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

    def test_validate_should_raise_validation_error_when_fixture_identifier_contains_path_split(self):
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


import unittest


class TestCompleter(unittest.TestCase):

    def test_directory_completer_should_expose_directory_in_autocomplete(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            fixture_repository = os.path.join(os.getcwd(), 'fixtup')

            # Acts
            completer = directory_completer(fixture_repository)

            # Assert
            self.assertEqual(['hello'], completer.words)


if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
