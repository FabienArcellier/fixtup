import os

import attr


@attr.s
class FixtureTemplate():
    identifier: str = attr.ib()
    directory: str = attr.ib()

    """
    This flag activate the keep_mounted policy. The fixture is mounted only once at the first test
    that use this fixture, then reused by each test.
    """
    keep_mounted: bool = attr.ib()

    """
    This flag activate the keep_running policy. The fiture keep running between each test. If you are
    using a container, it doesn't stop between 2 tests. The fixture is stop and unmount when the test process stop.
    """
    keep_running: bool = attr.ib()

    config: dict = attr.ib(factory=dict)

    @classmethod
    def create_from_cli(cls,
                        identifier: str,
                        fixture_repository: str) -> 'FixtureTemplate':
        directory = os.path.join(fixture_repository, identifier)
        return FixtureTemplate(identifier=identifier,
                               directory=directory,
                               keep_mounted=False,
                               keep_running=False)

    @classmethod
    def create_from_fixture_template(cls, path: str, fixture_yml: dict) -> 'FixtureTemplate':
        keep_mounted = fixture_yml.get('keep_mounted', False)
        keep_running = fixture_yml.get('keep_running', False)
        identifier = os.path.basename(path)
        return FixtureTemplate(identifier, path, keep_mounted, keep_running, config=fixture_yml)

    @classmethod
    def fake(cls, **kwargs):
        """
        build a fake entity to help design unit testing
        """
        identifier = kwargs.get('identifier', 'simple_database')
        directory = kwargs.get('directory', '/home/far/my_project/test/fixture')

        return FixtureTemplate(
            identifier=identifier,
            directory=os.path.join(directory, identifier),
            keep_mounted=kwargs.get('keep_mounted', False),
            keep_running=kwargs.get('keep_running', False),
        )

    def variables(self) -> dict:
        return attr.asdict(self)
