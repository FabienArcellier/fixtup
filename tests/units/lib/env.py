import os
import unittest

from fixtup.lib.env import env_override


class TestEnv(unittest.TestCase):
    def setUp(self):
        pass

    def test_env_override_should_set_a_new_environment_variable(self):
        # Arrange
        # Acts
        with env_override({
            "HELLO": "WORLD"
        }):
            self.assertEqual(os.getenv("HELLO"), "WORLD")

    def test_env_remove_added_environment_variable(self):
        # Arrange
        # Acts
        with env_override({
            "HELLO": "WORLD"
        }):
            pass

        self.assertNotIn("HELLO", os.environ)

    def test_env_override_should_replace_an_existing_environment_variable(self):
        # Arrange


        # Acts
        with env_override({
            "HELLO": "WORLD"
        }):
            self.assertEqual(os.getenv("HELLO"), "WORLD")


if __name__ == '__main__':
    unittest.main()
