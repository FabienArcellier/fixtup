import os

import unittest

import fixtup.helper
from fixtures import fixture_context


class TestHelper(unittest.TestCase):

    def setUp(self):
        if os.getenv('IGNORE_DOCKER_TESTS', '0') == '1':
            self.skipTest('this test use docker and is ignored on ci running windows because github action does not support docker on windows')

        self.context = fixture_context.setup_fake()
        self.context.emulate_new_process = True

    def tearDown(self) -> None:
        fixture_context.teardown_fake()

    def test_wait_port_should_raise_error_when_timeout_is_spend(self):
        # Assign
        # Acts
        try:
            fixtup.helper.wait_port(1234, timeout=500)
            self.fail('wait_port should raise error')
        except TimeoutError as exception:
            pass

    def test_wait_port_should_wait_redis_server_to_be_up(self):
        # Assign

        # Acts
        with fixtup.up('docker_redis'):
            fixtup.helper.wait_port(6379, timeout=60000)


if __name__ == '__main__':
    unittest.main()
