import os

import attr


@attr.s
class FixtureTemplate():
    identifier: str = attr.ib()
    directory: str = attr.ib()

    """
    This flag activate the keep_up policy. The fiture keep running between each test. If you are
    using a container, it doesn't stop between 2 tests. The fixture is stop and unmount when the test process stop.
    """
    keep_up: bool = attr.ib()

    """
    This flag control if a fixture is mount in temporary directory or if it's mounted in place in the fixture template
    directory directly.
    """
    mount_in_place: bool = attr.ib(default=False)

    config: dict = attr.ib(factory=dict)

    @classmethod
    def create_from_cli(cls,
                        identifier: str,
                        fixture_repository: str) -> 'FixtureTemplate':
        directory = os.path.join(fixture_repository, identifier)
        return FixtureTemplate(identifier=identifier,
                               directory=directory,
                               keep_up=False)

    @classmethod
    def create_from_fixture_template(cls, path: str, fixture_yml: dict) -> 'FixtureTemplate':
        keep_up = fixture_yml.get('keep_up', False)
        mount_in_place = fixture_yml.get('mount_in_place', False)
        identifier = os.path.basename(path)
        return FixtureTemplate(identifier, path,
                               config=fixture_yml,
                               keep_up=keep_up,
                               mount_in_place=mount_in_place)

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
            keep_up=kwargs.get('keep_up', False),
            mount_in_place=kwargs.get('mount_in_place', False),
        )

    def variables(self) -> dict:
        return attr.asdict(self)
