import os
import unittest

import fixtup
from fixtup.entity.fixture import Fixture, State
from fixtup.factory import RuntimeContext, reset_runtime_context
from fixtup.fixture.factory import lookup_fixture_engine
from fixtup.fixture_template.base import fixture_template


class TestFixtureEngine(unittest.TestCase):

    def setUp(self) -> None:
        reset_runtime_context(RuntimeContext(unittest=True))
        self.tested = lookup_fixture_engine()

    def test_new_fixture_should_create_an_empty_directory_in_tmp_file(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            template = fixture_template('hello')

            # Acts
            fixture = self.tested.new_fixture(template)

            # Assert
            self.assertEqual(State.Reserved, fixture.state)
            self.assertTrue(os.path.isdir(fixture.directory), f"{fixture.directory} should be a directory")

    def test_mount_should_copy_the_content_of_template_into_tmp_directory(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            template = fixture_template('hello')

            # Acts
            fixture = self.tested.new_fixture(template)
            self.tested.mount(template, fixture)

            # Assert
            self.assertEqual(State.Mounted, fixture.state)
            file_txt = os.path.join(fixture.directory, 'file.txt')
            self.assertTrue(os.path.isfile(file_txt), f"{file_txt} should be a file")

    def test_unmount_should_remove_the_fixture_directory(self):
        # Arrange
        with fixtup.up('fixtup_project'):
            template = fixture_template('hello')

            # Acts
            fixture = self.tested.new_fixture(template)
            self.tested.mount(template, fixture)
            self.tested.unmount(fixture)

            # Assert
            self.assertEqual(State.Unmounted, fixture.state)
            self.assertFalse(os.path.isdir(fixture.directory), f"{fixture.directory} should be a directory")


if __name__ == '__main__':
    unittest.main()
