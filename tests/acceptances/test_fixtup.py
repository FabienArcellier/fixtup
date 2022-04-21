import logging
import os
import shutil
import unittest

import fixtup
from fixtup.exceptions import FixtureNotFound, PluginRuntimeError
from fixtup.factory import reset_runtime_context, RuntimeContext
from fixtup.tests.logger import disable_logging
from fixtup.tests.settings import override_fixtup_settings


class TestFixtup(unittest.TestCase):

    def setUp(self):
        reset_runtime_context(RuntimeContext(unittest=True, enable_plugins=False, emulate_new_process=True))

    def tearDown(self) -> None:
        reset_runtime_context()

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

    def test_up_should_show_error_message_when_error_happens_in_plugins(self):
        reset_runtime_context(RuntimeContext(unittest=True, enable_plugins=True, emulate_new_process=True))
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))

        # Acts
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../fixtures/fixtup"),
            'plugins': [
                'fixtup.plugins.dummy_plugin_error'
            ]
        }):
            with disable_logging():
                # Assert
                try:
                    with fixtup.up('simple'):
                        cwd = os.getcwd()
                        self.fail('up should raise PluginRuntimeError')
                except PluginRuntimeError as exception:
                    self.assertIn('plugin: fixtup.plugins.dummy_plugin_error', exception.msg)

    def test_up_on_fixture_with_shared_policy_should_keep_the_same_fixture_environment(self):
        # self.skipTest("not implemented yet")

        reset_runtime_context(RuntimeContext(unittest=True, emulate_new_process=False))
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))

        # Acts
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../fixtures/fixtup"),
            'plugins': []
        }):
            # Acts
            with fixtup.up('simple_fixture_shared'):
                fixture1 = os.getcwd()

            with fixtup.up('simple_fixture_shared'):
                fixture2 = os.getcwd()

            # Assert
            self.assertEqual(fixture1, fixture2)

    def test_up_on_fixture_without_shared_policy_should_create_a_new_fixture_environment(self):
        SCRIPT_DIR = os.path.realpath(os.path.join(__file__, '..'))

        # Acts
        with override_fixtup_settings({
            "fixtures": os.path.join(SCRIPT_DIR, "../fixtures/fixtup"),
            'plugins': []
        }):
            # Acts
            with fixtup.up('simple_fixture_shared'):
                fixture1 = os.getcwd()

            with fixtup.up('simple_fixture_shared'):
                fixture2 = os.getcwd()

            # Assert
            self.assertNotEqual(fixture1, fixture2)


if __name__ == '__main__':
    unittest.main()
