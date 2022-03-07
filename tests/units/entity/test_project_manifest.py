import unittest

from fixtup.entity.project_manifest import ProjectManifests


class Test(unittest.TestCase):
    def setUp(self):
        self._tested = ()

    def test_create_from_path_should_create_one_project_manifest_by_manifest_path(self):
        # Arrange
        manifests_path = [
            "hello/setup.cfg",
            "hello/pyproject.toml",
        ]

        # Acts
        manifests = ProjectManifests.create_from_path(manifests_path)

        # Assert
        self.assertEqual(2, len(manifests))

    def test_prompt_should_send_a_list_of_choices(self):
        # Arrange
        manifests_path = [
            "hello/setup.cfg",
            "hello/pyproject.toml",
        ]
        manifests = ProjectManifests.create_from_path(manifests_path)

        # Acts
        choices = manifests.prompt_choices()

        # Assert
        self.assertEqual(2, len(choices))
        self.assertEqual('setup.cfg', choices[0])


if __name__ == '__main__':
    unittest.main()
