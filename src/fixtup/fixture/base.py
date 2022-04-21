import atexit
import contextlib
import os
import shutil
import signal
import tempfile
from typing import List, Optional, Any

import attr

from fixtup.entity.fixtup_process import FixtupProcess
from fixtup.entity.fixture import Fixture, State
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.exceptions import PluginRuntimeError
from fixtup.hook.base import HookEngine, HookEvent
from fixtup.lib.signal import register_signal_handler, unregister_signal_handler
from fixtup.logger import get_logger
from fixtup.plugin.base import PluginEngine, PluginEvent


@attr.s
class FixtureEngine:
    hook_engine: HookEngine = attr.ib()
    plugin_engine: PluginEngine = attr.ib()
    store: FixtupProcess = attr.ib()

    def __attrs_post_init__(self):
        self.register_process_teardown()

    def mount(self, fixture_template: FixtureTemplate, fixture: Fixture) -> None:
        assert fixture_template.identifier == fixture.template_identifier

        # When a fixture is shared and already mounted
        # then we only change the working directory path
        if self.store.is_mounted(fixture_template):
            os.chdir(fixture.directory)
            return

        try:
            shutil.copytree(fixture_template.directory, fixture.directory)
            # restore the directory after having removing the old one
            os.chdir(fixture.directory)

            self.plugin_engine.run(PluginEvent.mounting, fixture)
            self.hook_engine.run(HookEvent.mounting, fixture_template)
            self.store.fixture_mounted(fixture_template, fixture)
        except PluginRuntimeError:
            self.plugin_engine.release(PluginEvent.unmounting, fixture)
            if os.path.isdir(fixture.directory):
                shutil.rmtree(fixture.directory, True)

            raise

    def new_fixture(self, fixture_template: FixtureTemplate) -> Fixture:
        if self.store.is_mounted(fixture_template):
            fixture = self.store.fixture(fixture_template)

            assert fixture_template.shared is True, f"fixture {fixture.identifier} is mounted but should not, the template does not use shared policy"
            return fixture

        tmp_prefix = '{0}_{1}'.format(fixture_template.identifier, '_')
        fixture_directory = tempfile.mkdtemp(prefix=tmp_prefix)
        os.rmdir(fixture_directory)

        return Fixture.create_from_template(fixture_template, fixture_directory)

    def process_teardown_exit(self):
        self._teardown()

    def process_teardown_signal(self, code: int, frame: Any):
        logger = get_logger()
        logger.info(f'user interruption through os signal {code}, tear down mounted fixtures')
        self._teardown()

    def _teardown(self):
        for template, fixture in self.store.mounted_fixtures():
            if fixture.state == State.Started:
                self.stop(template, fixture, teardown=True)
            self.unmount(template, fixture, teardown=True)

    def start(self, template: FixtureTemplate, fixture: Fixture) -> None:
        try:
            self.plugin_engine.run(PluginEvent.starting, fixture)
            self.hook_engine.run(HookEvent.starting, template)
            self.store.fixture_started(fixture)
        except PluginRuntimeError:
            self.plugin_engine.release(PluginEvent.stopping, fixture)
            self.plugin_engine.release(PluginEvent.unmounting, fixture)
            if os.path.isdir(fixture.directory):
                shutil.rmtree(fixture.directory, True)

            raise

    @contextlib.contextmanager
    def run(self, template: FixtureTemplate, fixture: Fixture):
        logger = get_logger()
        try:
            self.start(template, fixture)
            logger.debug(f'start fixture: {fixture.directory}')
            yield

        finally:
            logger.debug(f'stop fixture : {fixture.directory}')
            self.stop(template, fixture)

    def stop(self, template: FixtureTemplate, fixture: Fixture, teardown: bool = False) -> None:
        """

        :param teardown: true when the fixture engine is tear downed at the end of the process usually
        """
        try:
            self.plugin_engine.run(PluginEvent.stopping, fixture)
            self.hook_engine.run(HookEvent.stopping, template)
            self.store.fixture_stopped(fixture)
        except PluginRuntimeError:
            self.plugin_engine.release(PluginEvent.unmounting, fixture)
            if os.path.isdir(fixture.directory):
                shutil.rmtree(fixture.directory, True)

            raise

    def unmount(self, template: FixtureTemplate, fixture: Fixture, teardown: bool = False) -> None:
        """

        :param teardown: true when the fixture engine is tear downed at the end of the process usually
        """
        if template.shared is True and not teardown:
            return

        self.plugin_engine.run(PluginEvent.unmounting, fixture)
        self.hook_engine.run(HookEvent.unmounting, template)

        shutil.rmtree(fixture.directory, True)
        self.store.fixture_unmounted(fixture)

    @contextlib.contextmanager
    def use(self, template: FixtureTemplate, keep_mounted_fixture: bool = False):
        logger = get_logger()
        fixture = self.new_fixture(template)
        try:
            self.mount(template, fixture)
            logger.debug(f'mount fixture directory: {fixture.directory}')
            yield fixture

        finally:
            if not keep_mounted_fixture:
                logger.debug(f'remove mounted fixture directory : {fixture.directory}')
                self.unmount(template, fixture)

    def register_process_teardown(self):
        """
        register cleanup callbacks to unmount fixtures always mounted
        at the end of the test runtime execution

        Mounted fixtures are usually :

        * fixture with shared policy
        """
        atexit.register(self.process_teardown_exit)
        register_signal_handler(signal.SIGTERM, self.process_teardown_signal)
        register_signal_handler(signal.SIGQUIT, self.process_teardown_signal)

    def unregister_process_teardown(self):
        """
        unregister cleanup callbacks if cleanup was triggered
        manually
        """
        atexit.unregister(self.process_teardown_exit)
        unregister_signal_handler(signal.SIGTERM, self.process_teardown_signal)
        unregister_signal_handler(signal.SIGQUIT, self.process_teardown_signal)
