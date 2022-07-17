import atexit
import contextlib
import os
import shutil
import signal
import tempfile
from typing import Any

import attr

from fixtup.entity.fixtup_process import FixtupProcess
from fixtup.entity.fixture import Fixture, State
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.exceptions import PluginRuntimeError, HookRuntimeError
from fixtup.hook.base import HookEngine, HookEvent
from fixtup.lib.env import with_cwd
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

    def new_fixture(self, fixture_template: FixtureTemplate) -> Fixture:
        if self.store.is_up(fixture_template):
            fixture = self.store.fixture(fixture_template)

            assert fixture_template.keep_up is True, \
                f"fixture {fixture.identifier} is mounted but should not, the template does not use keep_mounted policy"
            return fixture

        if fixture_template.mount_in_place:
            fixture_directory = fixture_template.directory
        else:
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
        for template, fixture in self.store.active_fixtures():
            if fixture.state == State.Ready:
                self.teardown_data(template, fixture, process_teardown=True)

            if fixture.state == State.Up:
                self.stop(template, fixture, process_teardown=True)

    @contextlib.contextmanager
    def run(self, template: FixtureTemplate, keep_mounted_fixture: bool = False):
        """
        mount and execute a fixture from a template

        :param template:
        :param keep_mounted_fixture:
        :return:
        """
        logger = get_logger()
        fixture = self.new_fixture(template)
        try:
            self.start(template, fixture)
            self.setup_data(template, fixture)
            logger.debug(f'start fixture: {fixture.directory}')
            if template.mount_in_place is False:
                with with_cwd(fixture.directory):
                    yield
            else:
                yield

        finally:
            if fixture.state == State.Ready:
                self.teardown_data(template, fixture)

            logger.debug(f'stop fixture : {fixture.directory}')
            if fixture.state == State.Up:
                self.stop(template, fixture, keep_mounted_fixture=keep_mounted_fixture)

    def setup_data(self, template: FixtureTemplate, fixture: Fixture) -> None:
        with with_cwd(fixture.directory):
            try:
                self.plugin_engine.run(PluginEvent.setup_data, fixture)
                self.hook_engine.run(HookEvent.setup_data, template)
                fixture.setup_data()
            except (PluginRuntimeError, HookRuntimeError):
                self.plugin_engine.release(PluginEvent.teardown_data, fixture)
                self.plugin_engine.release(PluginEvent.stopping, fixture)

                # When a fixture is mount in place, Fixtup should preserve the original
                # when error happens
                if not template.mount_in_place and os.path.isdir(fixture.directory):
                    shutil.rmtree(fixture.directory, True)

                raise

    def start(self, template: FixtureTemplate, fixture: Fixture) -> None:
        assert template.identifier == fixture.template_identifier

        if self.store.is_up(template):
            return

        if not template.mount_in_place:
            shutil.copytree(template.directory, fixture.directory)

        with with_cwd(fixture.directory):
            try:
                os.chdir(fixture.directory)
                self.plugin_engine.run(PluginEvent.starting, fixture)
                self.hook_engine.run(HookEvent.starting, template)
                self.store.fixture_up(template, fixture)
            except (PluginRuntimeError, HookRuntimeError):
                self.plugin_engine.release(PluginEvent.stopping, fixture)

                # When a fixture is mount in place, Fixtup should preserve the original
                # when error happens
                if not template.mount_in_place and os.path.isdir(fixture.directory):
                    shutil.rmtree(fixture.directory, True)

                raise

    def stop(self, template: FixtureTemplate, fixture: Fixture,
             process_teardown: bool = False,
             keep_mounted_fixture: bool = False) -> None:
        """
        Stop and remove the fixture if it's the end of the test or
        when all the tests have been played if the fixture should be kept up.

        :param process_teardown: true when the fixture engine is tear downed at the end of the process usually
        """
        if template.keep_up is True and not process_teardown:
            return

        with with_cwd(fixture.directory):
            try:
                self.plugin_engine.run(PluginEvent.stopping, fixture)
                self.hook_engine.run(HookEvent.stopping, template)
                self.store.fixture_down(fixture)
            finally:
                # When a fixture is mount in place, Fixtup should preserve the original
                # when error happens
                if keep_mounted_fixture is False and \
                    not template.mount_in_place and \
                    os.path.isdir(fixture.directory):
                    shutil.rmtree(fixture.directory, True)

    def register_process_teardown(self):
        """
        register cleanup callbacks to unmount fixtures always mounted
        at the end of the test runtime execution

        Mounted fixtures are usually :

        * fixture with keep_up policy
        """
        atexit.register(self.process_teardown_exit)
        register_signal_handler(signal.SIGTERM, self.process_teardown_signal)
        register_signal_handler(signal.SIGQUIT, self.process_teardown_signal)

    def teardown_data(self, template, fixture, process_teardown: bool = False):
        """

        :param process_teardown: true when the fixture engine is tear downed at the end of the process usually
        """
        with with_cwd(fixture.directory):
            self.plugin_engine.run(PluginEvent.teardown_data, fixture)
            self.hook_engine.run(HookEvent.teardown_data, fixture)
            fixture.teardown_data()

    def unregister_process_teardown(self):
        """
        unregister cleanup callbacks if cleanup was triggered
        manually
        """
        atexit.unregister(self.process_teardown_exit)
        unregister_signal_handler(signal.SIGTERM, self.process_teardown_signal)
        unregister_signal_handler(signal.SIGQUIT, self.process_teardown_signal)
