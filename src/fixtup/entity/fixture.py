import os

import attr

@attr.s
class Fixture():
    identifier: str = attr.ib()
    directory: str = attr.ib()
    shared: bool = attr.ib()

    config: dict = attr.ib(factory=dict)

    @classmethod
    def create_from_cli(cls, identifier: str, fixture_repository: str, shared: bool) -> 'Fixture':
        directory = os.path.join(fixture_repository, identifier)
        return Fixture(identifier=identifier, directory=directory, shared=shared)
