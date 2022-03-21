import unittest

from fixtup.hook.base import HookEvent
from fixtup.hook.python import script
from fixtup.lib.enum import enum_values


class TestPython(unittest.TestCase):
    def setUp(self):
        pass

    def test_script_implement_all_the_events(self):
        # Arrange
        events = enum_values(HookEvent)

        # Acts
        for event in events:
            with self.subTest(event):
                file = script(event)

                # Assert
                self.assertIsNotNone(file)


if __name__ == '__main__':
    unittest.main()
