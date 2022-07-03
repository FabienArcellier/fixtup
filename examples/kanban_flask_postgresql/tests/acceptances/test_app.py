import unittest

from flask import Response

import fixtup

from kanban.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self) -> None:
        pass

    def test_put_should_move_work_item_in_a_new_column(self):
        with fixtup.up('pgsql'):
            with fixtup.up('simple_board'):
                # Arrange
                self.client.put("/work_item/4", json={
                    'column': 2,
                    'title': "implement feature XXX",
                    'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam "
                                   "augue nunc, cursus nec diam eget, pretium iaculis turpis. Sed quis convallis massa.",
                })

                # Acts
                response: Response = self.client.get("/work_item/4")

                # Assert
                self.assertEqual(2, response.json['column'])

    def test_put_work_item_in_a_new_column_should_fail_when_wip_limit_is_already_reached(self):
        with fixtup.up('pgsql'):
            with fixtup.up('simple_board_with_wip'):
                # Arrange
                response_mutation: Response = self.client.put("/work_item/5", json={
                    'column': 3,
                    'title': "implement feature XXX",
                    'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam "
                                   "augue nunc, cursus nec diam eget, pretium iaculis turpis. Sed quis convallis massa.",
                })

                # Acts
                response_query: Response = self.client.get("/work_item/5")

                # Assert
                json_mutation = response_mutation.json
                self.assertFalse(json_mutation['ok'])

                json_query = response_query.json
                self.assertEqual(1 , json_query['column'])

    def test_post_work_item_should_add_a_new_work_item(self):
        with fixtup.up('pgsql'):
            with fixtup.up('simple_board'):
                # Arrange

                # Acts
                response_mutation: Response = self.client.post("/work_item", json={
                    'column': 3,
                    'title': "implement feature ZZZ",
                    'description': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam "
                                   "augue nunc, cursus nec diam eget, pretium iaculis turpis. Sed quis convallis massa.",
                })

                # Assert
                self.assertEqual(200, response_mutation.status_code)

                json_mutation = response_mutation.json
                self.assertTrue(json_mutation['ok'])
                self.assertEqual('implement feature ZZZ', json_mutation['data']['title'])
                self.assertIsNotNone(json_mutation['data']['pid'])



if __name__ == '__main__':
    unittest.main()
