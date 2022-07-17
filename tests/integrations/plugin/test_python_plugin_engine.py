import os
import unittest

import fixtup
from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.exceptions import PluginRuntimeError
from fixtup.plugin.base import PluginEvent
from fixtup.plugin.python import PythonPluginEngine


class TestPythonPluginBase(unittest.TestCase):
    def setUp(self):
        self._tested = PythonPluginEngine()

    def test_run_should_execute_the_plugin_event_for_event_handler_that_requires_fixture(self):
        events = {
            PluginEvent.setup_data: "setup_data.txt",
            PluginEvent.starting: "starting.txt",
            PluginEvent.stopping: "stopping.txt",
            PluginEvent.teardown_data: "teardown_data.txt"
        }

        self._tested.register_plugin('fixtup.plugins.dummy_plugin')

        for event in events:
            with self.subTest(event):
                with fixtup.up('simple'):
                    # Arrange
                    fixture = Fixture.fake(directory=os.getcwd())

                    # Acts
                    self._tested.run(event, fixture=fixture)

                    # Assert
                    file_to_check = events[event]
                    file_is_present = os.path.isfile(os.path.join(os.getcwd(), file_to_check))
                    self.assertTrue(file_is_present, f'{file_to_check} must be present in {os.getcwd()}')

    def test_run_should_execute_the_plugin_event_for_event_handler_that_requires_template(self):
        events = {
            PluginEvent.new_fixture: "new_fixture.txt",
        }

        self._tested.register_plugin('fixtup.plugins.dummy_plugin')
        template = FixtureTemplate.fake()

        for event in events:
            with self.subTest(event):
                with fixtup.up('simple'):
                    # Arrange
                    # Acts
                    self._tested.run(event, template=template)

                    # Assert
                    file_to_check = events[event]
                    file_is_present = os.path.isfile(os.path.join(os.getcwd(), file_to_check))
                    self.assertTrue(file_is_present, f'{file_to_check} must be present in {os.getcwd()}')


    def test_run_should_raise_plugin_exception_error(self):
        self._tested.register_plugin('fixtup.plugins.dummy_plugin_error')

        with fixtup.up('simple'):
            # Arrange
            fixture = Fixture.fake()
            # Acts
            try:
                self._tested.run(PluginEvent.starting, fixture=fixture)
                self.fail("this test should raise PluginRuntimeError")
            except PluginRuntimeError as exception:
                pass


if __name__ == '__main__':
    unittest.main()
