import os
import unittest

import fixtup

import kanban.database


class Test(unittest.TestCase):

    def test_init_db_should_create_schema_into_sqlite(self):
        # Arrange
        with fixtup.up('simple_board'):
            # Acts
            kanban.database.db_init()

            # Assert
            db_path = os.path.join(os.getcwd(), 'kanban.db')
            self.assertTrue(os.path.isfile(db_path))


if __name__ == '__main__':
    unittest.main()
