import os
import shutil
import unittest

import fixtup
from fixtup.exceptions import FixtureNotFound


class TestFixtup(unittest.TestCase):
    def setUp(self):
        pass

    def test_up_should_mount_a_fixture_into_tmp_file(self):
        # Arrange
        # Acts & Assert
        with fixtup.up('simple'):
            cwd = os.getcwd()
            self.assertTrue(os.path.isdir(cwd))
            self.assertTrue(os.path.isfile(os.path.join(cwd, 'hello.txt')))

    def test_up_should_remove_the_mounted_fixture_outside_the_context(self):
        # Acts & Assert
        with fixtup.up('simple'):
            cwd = os.getcwd()

        self.assertFalse(os.path.isdir(cwd))

    def test_up_move_the_working_dir_into_mounted_fixture(self):
        # Acts & Assert
        working_dir = os.getcwd()

        with fixtup.up('simple'):
            cwd = os.getcwd()
            self.assertNotEqual(working_dir, cwd)

    def test_up_restore_the_working_dir_outside_the_context(self):
        # Acts & Assert
        working_dir = os.getcwd()

        with fixtup.up('simple'):
            pass

        self.assertEqual(working_dir, os.getcwd())

    def test_up_should_keep_the_mounted_fixture_if_the_flag_keep_mounted_fixture_is_present(self):
        # Acts & Assert
        with fixtup.up('simple', keep_mounted_fixture=True):
            cwd = os.getcwd()

        self.assertTrue(os.path.isdir(cwd))

        # clean up
        shutil.rmtree(cwd)

    def test_up_should_raise_fixture_not_found_when_fixture_is_missing(self):
        # Acts & Assert
        try:
            with fixtup.up('other') as wd:
                self.fail('up should raise FixtureNotFound exception because this fixture does not exists')
        except FixtureNotFound:
                pass

    def test_configure_should_override_manifest_settings(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))

        # Acts
        fixtup.configure({"fixtures": os.path.join(SCRIPT_DIR, "../fixtures/fixtup")})

        # Assert
        with fixtup.up('simple'):
            cwd = os.getcwd()
            self.assertTrue(os.path.isdir(cwd))
            self.assertTrue(os.path.isfile(os.path.join(cwd, 'hello.txt')))




if __name__ == '__main__':
    unittest.main()
