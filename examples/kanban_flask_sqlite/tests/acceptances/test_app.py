import unittest

from flask import Response

import fixtup

from kanban.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_put_should_move_work_item_in_a_new_column(self):
        with fixtup.up('simple_board'):
            # Arrange
            self.client.put("/work_item/12", json={
                'column': 2,
                'title': "implement feature XXX",
                'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam "
                               "augue nunc, cursus nec diam eget, pretium iaculis turpis. Sed quis convallis massa.",
            })

            # Acts
            response: Response = self.client.get("/work_item/12")

            # Assert
            self.assertEqual(2, response.json['column'])


if __name__ == '__main__':
    unittest.main()
