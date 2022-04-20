import contextlib
import os
import shutil
import tempfile

import attr

from fixtup.entity.fixtup_process import FixtupProcess
from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate
from fixtup.exceptions import PluginRuntimeError
from fixtup.hook.base import HookEngine, HookEvent
from fixtup.logger import get_logger
from fixtup.plugin.base import PluginEngine, PluginEvent


@attr.s
class FixtureEngine:
    hook_engine: HookEngine = attr.ib()
    plugin_engine: PluginEngine = attr.ib()
    store: FixtupProcess = attr.ib()

    def mount(self, fixture_template: FixtureTemplate, fixture: Fixture) -> None:
        assert fixture_template.identifier == fixture.template_identifier

        # Quand une fixture est partagée et qu'elle est déjà montée
        # alors on change seulement le chemin du working directory
        if self.store.is_mounted(fixture_template):
            os.chdir(fixture.directory)
            return

        try:
            shutil.copytree(fixture_template.directory, fixture.directory)
            # restore the directory after having removing the old one
            os.chdir(fixture.directory)

            self.plugin_engine.run(PluginEvent.mounting, fixture)
            self.hook_engine.run(HookEvent.mounting, fixture_template)
            self.store.fixture_mounted(fixture)
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

    def stop(self, template: FixtureTemplate, fixture: Fixture) -> None:
        try:
            self.plugin_engine.run(PluginEvent.stopping, fixture)
            self.hook_engine.run(HookEvent.stopping, template)
            self.store.fixture_stopped(fixture)
        except PluginRuntimeError:
            self.plugin_engine.release(PluginEvent.unmounting, fixture)
            if os.path.isdir(fixture.directory):
                shutil.rmtree(fixture.directory, True)

            raise

    def unmount(self, template: FixtureTemplate, fixture: Fixture) -> None:
        if template.shared is True:
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
