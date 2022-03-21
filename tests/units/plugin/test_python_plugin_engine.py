import logging
import unittest

from fixtup.logger import get_logger
from fixtup.plugin.python import PythonPluginEngine


class TestPythonPluginEngine(unittest.TestCase):

    def setUp(self):
        logger = get_logger()
        self._tested = PythonPluginEngine()

    def tearDown(self) -> None:
        logger = get_logger()

    def test_register_plugin_should_register_the_plugin(self):
        # Arrange
        # Acts
        self._tested.register_plugin('fixtup.plugins.dummy_plugin')

        # Assert
        self.assertEqual(1, len(self._tested.plugins))

    def test_register_plugin_should_ignore_plugin_not_found_with_error_message(self):
        # Arrange
        # Acts
        with self.assertLogs(level='INFO') as log:
            self._tested.register_plugin('yolo_plugins')

            # Assert
            self.assertEqual(0, len(self._tested.plugins))

            self.assertEqual(1, len(log.output))


if __name__ == '__main__':
    unittest.main()
