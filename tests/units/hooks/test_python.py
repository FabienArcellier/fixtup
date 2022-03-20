import unittest

from fixtup.hook.base import HookEvent
from fixtup.hook.python import script


class TestPython(unittest.TestCase):
    def setUp(self):
        pass

    def test_script_implement_all_the_events(self):
        # Arrange
        events = HookEvent.values()

        # Acts
        for event in events:
            with self.subTest(event):
                file = script(event)

                # Assert
                self.assertIsNotNone(file)


if __name__ == '__main__':
    unittest.main()
