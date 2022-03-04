import unittest

import fixtup
from fixtup.exceptions import PythonManifestMissing
from fixtup.settings.base import list_project_manifests


class TestBase(unittest.TestCase):
    def setUp(self):
        pass

    def test_list_project_manifests_should_return_both_manifests_if_both_are_present(self):
        # Arrange
        with fixtup.up('manifests'):
            # Acts
            _available_manifests = list_project_manifests()

            # Assert
            self.assertEqual(['setup.cfg', 'pyproject.toml'], _available_manifests)

    def test_list_project_manifests_should_raise_exception_if_no_manifest_exists(self):
        # Arrange
        with fixtup.up('manifests_missing'):
            # Acts
            try:
                _available_manifests = list_project_manifests()
                self.fail('python manifest is missing, this test should raise an exception')
            # Assert
            except PythonManifestMissing as exception:
                pass




if __name__ == '__main__':
    unittest.main()
