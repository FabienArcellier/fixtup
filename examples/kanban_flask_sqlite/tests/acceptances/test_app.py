import unittest

from flask import Response

import fixtup

import kanban.database
from kanban.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self) -> None:
        kanban.database.db_dispose()

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

    def test_put_work_item_in_a_new_column_should_fail_when_wip_limit_is_already_reached(self):
        with fixtup.up('simple_board_with_wip'):
            # Arrange
            response_mutation: Response = self.client.put("/work_item/12", json={
                'column': 3,
                'title': "implement feature XXX",
                'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam "
                               "augue nunc, cursus nec diam eget, pretium iaculis turpis. Sed quis convallis massa.",
            })

            # Acts
            response_query: Response = self.client.get("/work_item/12")

            # Assert
            json_mutation = response_mutation.json
            self.assertFalse(json_mutation['ok'])

            json_query = response_query.json
            self.assertEqual(1 , json_query['column'])



if __name__ == '__main__':
    unittest.main()
