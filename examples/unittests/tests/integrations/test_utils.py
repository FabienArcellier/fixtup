import unittest
import os

import fixtup

from lib.utils import thumbnail


class UtilsTest(unittest.TestCase):

    def test_thumbnail_should_generate_thumbnail(self):
        with fixtup.up('thumbnail_context'):
            # Given
            wd = os.getcwd()

            original_file = os.path.join(wd, 'file.png')
            expected_thumbnail_file = os.path.join(wd, 'file_t.png')

            # When
            thumbnail(original_file, expected_thumbnail_file)

            # Then
            self.assertTrue(os.path.isfile(expected_thumbnail_file))
