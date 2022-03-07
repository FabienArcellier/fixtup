import os
from typing import List, Optional

import attr


@attr.s
class ProjectManifest:
    identifier : str = attr.ib()
    path: str = attr.ib()

    def __attrs_post_init__(self):
        assert os.path.isabs(self.path), f"{self} manifest location should be an absolute path"

    @classmethod
    def create_from_path(cls, manifest_path: str) -> 'ProjectManifest':
        """

        >>> ProjectManifest.create_from_path("/home/far/hello/setup.cfg")

        >>> ProjectManifest.create_from_path("hello/setup.cfg")

        :param manifest_path:
        """
        _manifest_path = os.path.abspath(manifest_path)
        identifier = os.path.basename(manifest_path)

        return ProjectManifest(identifier, _manifest_path)

@attr.s
class ProjectManifests:
    manifests: List[ProjectManifest] = attr.ib()

    @classmethod
    def create_from_path(cls, manifests: List[str]) -> 'ProjectManifests':
        _manifests: List[ProjectManifest] = []
        for manifest_path in manifests:
            _manifests.append(ProjectManifest.create_from_path(manifest_path))

        return ProjectManifests(_manifests)

    def __len__(self):
        return len(self.manifests)

    def prompt_choices(self) -> List[str]:
        """
        gets the list of choices to display to the user when they have to choose
        a manifest to for example configure the settings of a fixtup project
        """

        return [manifest.identifier for manifest in self.manifests]

    def missing(self) -> bool:
        """
        determines if project manifests exist for a python project
        """
        return len(self.manifests) == 0

    def get(self, manifest_choice: str):
        for manifest in self.manifests:
            if manifest_choice == manifest.identifier:
                return manifest

        raise ValueError(f"this choice does not match any manifest - {self.manifests}")


