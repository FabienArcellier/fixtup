import os
import unittest

from fixtup import fixtup
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.hook.base import HookEvent
from fixtup.hook.python import PythonHookEngine


class TestPythonHookEngine(unittest.TestCase):
    def setUp(self):
        self._tested = PythonHookEngine()

    def test_run_should_invoke_the_hook_relative_to_mounted_event(self):
        with fixtup.up("fixtup_hook"):
            # Arrange
            template = FixtureTemplate.fake(
                directory=os.path.join(os.getcwd(), 'fixtup', 'hello')
            )

            # Acts
            self._tested.run(HookEvent.mounted, template)

            # Assert
            fake_mounted_file_existing = os.path.join(os.getcwd(), 'mounted')
            self.assertTrue(os.path.isfile(fake_mounted_file_existing), f'{fake_mounted_file_existing} has to exists')


if __name__ == '__main__':
    unittest.main()

