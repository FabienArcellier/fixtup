import os

import attr

@attr.s
class FixtureTemplate():
    identifier: str = attr.ib()
    directory: str = attr.ib()
    shared: bool = attr.ib()

    config: dict = attr.ib(factory=dict)

    @classmethod
    def create_from_cli(cls, identifier: str, fixture_repository: str, shared: bool) -> 'FixtureTemplate':
        directory = os.path.join(fixture_repository, identifier)
        return FixtureTemplate(identifier=identifier, directory=directory, shared=shared)

    @classmethod
    def create_from_fixture_template(cls, path: str, fixture_yml: dict) -> 'FixtureTemplate':
        is_shared = fixture_yml.get('shared', False)
        identifier = os.path.basename(path)
        return FixtureTemplate(identifier, path, is_shared, config=fixture_yml)

    @classmethod
    def fake(cls, **kwargs):
        """
        build a fake entity to help design unit testing
        """

        return FixtureTemplate(
            identifier=kwargs.get('identifier', 'simple_database'),
            directory=kwargs.get('directory', '/home/far/my_project/test/fixture/simple_database'),
            shared=kwargs.get('shared', False)
        )
