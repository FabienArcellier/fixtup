import os
import shutil
import tempfile
from typing import Any

import attr

from fixtup.entity.fixtup_process import FixtupProcess
from fixtup.entity.fixture import Fixture
from fixtup.entity.fixture_template import FixtureTemplate


@attr.s
class FixtureEngine:
    hook_engine: Any = attr.ib()
    plugin_engine: Any = attr.ib()
    store: FixtupProcess = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.store = FixtupProcess()

    def mount(self, fixture_template: FixtureTemplate, fixture: Fixture) -> None:
        assert fixture_template.identifier == fixture.template_identifier

        os.rmdir(fixture.directory)
        shutil.copytree(fixture_template.directory, fixture.directory)
        self.plugin_engine.run('MOUNTED', fixture)
        self.hook_engine.run('MOUNTED', fixture)
        self.store.fixture_mounted(fixture)

    def new_fixture(self, fixture_template) -> Fixture:
        tmp_prefix = '{0}_{1}'.format(fixture_template.identifier, '_')
        fixture_directory = tempfile.mkdtemp(prefix=tmp_prefix)

        return Fixture.create_from_template(fixture_template, fixture_directory)

    def start(self, fixture: Fixture) -> None:
        self.plugin_engine.run('STARTED', fixture)
        self.hook_engine.run('STARTED', fixture)
        self.store.fixture_started(fixture)

    def stop(self, fixture: Fixture) -> None:
        self.plugin_engine.run('STOPPED', fixture)
        self.hook_engine.run('STOPPED', fixture)
        self.store.fixture_stopped(fixture)

    def unmount(self, fixture: Fixture) -> None:
        self.plugin_engine.run('UNMOUNTED', fixture)
        self.hook_engine.run('UNMOUNTED', fixture)

        shutil.rmtree(fixture.directory, True)
        self.store.fixture_unmounted(fixture)


def mount(template: 'FixtureTemplate') -> None:
    tmp_prefix = '{0}_{1}'.format(template.identifier, '_')
    mounted_fixture = tempfile.mktemp(prefix=tmp_prefix)
    fixture = Fixture.create_from_template(template, mounted_fixture)
    shutil.copytree(template.directory, mounted_fixture)


def start(template: 'FixtureTemplate') -> None:
    raise NotImplementedError()


def stop(template: 'FixtureTemplate') -> None:
    raise NotImplementedError()


def unmount(template: 'FixtureTemplate', force: bool = False) -> None:
    raise NotImplementedError()


def is_mounted(template: 'FixtureTemplate') -> None:
    raise NotImplementedError()


def termination_handler() -> None:
    raise NotImplementedError()
