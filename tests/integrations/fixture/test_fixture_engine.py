import logging

import os
import unittest

from fixtup.context import lib_context_inject, lib_context_eject, lib_context_setup, lib_context_teardown
from fixtup.entity.fixture import State
from fixtup.fixture.factory import lookup_fixture_engine
from fixtup.fixture_template.base import fixture_template



class TestFixtureEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.context = lib_context_inject()
        self.context.emulate_new_process = True
        self.context.fixturesdir = os.path.realpath(os.path.join(__file__, '..', '..', '..', 'fixtures', 'fixtup'))
        lib_context_setup()

        logging.disable(logging.WARNING)
        self.tested = lookup_fixture_engine()


    def tearDown(self) -> None:
        lib_context_eject()
        lib_context_teardown()
        logging.disable(logging.INFO)

    def test_new_fixture_should_create_an_empty_directory_in_tmp_file(self):
        # Arrange
        template = fixture_template('simple_fixture')
        fixture = None
        try:
            # Acts
            fixture = self.tested.new_fixture(template)

            # Assert
            self.assertEqual(State.Down, fixture.state)
            self.assertFalse(os.path.isdir(fixture.directory), f"{fixture.directory} should be a directory")
        finally:
            if fixture is not None and os.path.isdir(fixture.directory):
                os.removedirs(fixture.directory)

    def test_new_fixture_from_template_keep_the_fixture_up(self):
        # Arrange
        try:
            template = fixture_template('simple_fixture_keep_up')
            # Acts
            fixture1 = self.tested.new_fixture(template)
            self.tested.start(template, fixture1)
            self.tested.stop(template, fixture1)

            fixture2 = self.tested.new_fixture(template)

            # Assert
            self.assertEqual(State.Up, fixture1.state)
            self.assertIs(fixture1, fixture2)
        finally:
            self.tested.process_teardown_exit()

    def test_new_fixture_from_template_keep_the_fixture_up_with_legacy_policy(self):
        # Arrange
        try:
            template = fixture_template('simple_fixture_keep_running_legacy')
            # Acts
            fixture1 = self.tested.new_fixture(template)
            self.tested.start(template, fixture1)
            self.tested.stop(template, fixture1)

            fixture2 = self.tested.new_fixture(template)

            # Assert
            self.assertEqual(State.Up, fixture1.state)
            self.assertIs(fixture1, fixture2)
        finally:
            self.tested.process_teardown_exit()

    def test_new_fixture_from_template_keep_the_fixture_running(self):
        # Arrange
        try:
            template = fixture_template('simple_fixture_keep_up')

            # Acts
            fixture1 = self.tested.new_fixture(template)
            self.tested.start(template, fixture1)
            self.tested.stop(template, fixture1)

            fixture2 = self.tested.new_fixture(template)

            # Assert
            self.assertEqual(State.Up, fixture1.state)
            self.assertIs(fixture1, fixture2)
        finally:
            self.tested.process_teardown_exit()

    def test_start_should_copy_the_content_of_template_into_tmp_directory(self):
        # Arrange
        template = fixture_template('simple')
        fixture = self.tested.new_fixture(template)
        try:
            # Acts
            self.tested.start(template, fixture)

            # Assert
            self.assertEqual(State.Up, fixture.state)
            file_txt = os.path.join(fixture.directory, 'hello.txt')
            self.assertTrue(os.path.isfile(file_txt), f"{file_txt} should be a file")
        finally:
            self.tested.stop(template, fixture)

    def test_start_should_use_template_directory_when_the_fixture_is_mount_in_place(self):
        # Arrange
        template = fixture_template('simple_fixture_mount_in_place')
        fixture = self.tested.new_fixture(template)
        try:
            # Acts
            self.tested.start(template, fixture)

            # Assert
            self.assertEqual(State.Up, fixture.state)
            self.assertEqual(template.directory, fixture.directory)
        finally:
            self.tested.stop(template, fixture)

    def test_process_teardown_exit_should_remove_the_fixture_directory_for_fixture_with_keep_up_policy(self):
        # Arrange
        template = fixture_template('simple_fixture_keep_up')
        fixture = self.tested.new_fixture(template)

        self.tested.start(template, fixture)

        # this instruction should have no effect
        self.tested.stop(template, fixture)

        self.assertEqual(State.Up, fixture.state)
        self.assertTrue(os.path.isdir(fixture.directory), f"{fixture.directory} should be a directory")

        # Acts
        self.tested.process_teardown_exit()

        # Assert
        self.assertEqual(State.Down, fixture.state)
        self.assertFalse(os.path.isdir(fixture.directory), f"{fixture.directory} should not be a directory")

    def test_stop_should_remove_the_fixture_directory(self):
        # Arrange
        template = fixture_template('simple')
        fixture = self.tested.new_fixture(template)
        self.tested.start(template, fixture)

        # Acts
        self.tested.stop(template, fixture)

        # Assert
        self.assertEqual(State.Down, fixture.state)
        self.assertFalse(os.path.isdir(fixture.directory), f"{fixture.directory} should not be a directory")


if __name__ == '__main__':
    unittest.main()
