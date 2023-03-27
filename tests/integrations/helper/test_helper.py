import unittest

import fixtup.helper


class TestHelper(unittest.TestCase):
    def setUp(self):
        pass

    def test_wait_readiness_should_detect_webserver(self):
        # Assign
        with fixtup.up("docker_webserver"):
            # Acts
            fixtup.helper.wait_readiness("http://localhost:8888", timeout=5000)

            # Assert

    def test_wait_readiness_should_detect_404_on_webserver_with_custom_predicate(self):
        # Assign
        with fixtup.up("docker_webserver"):
            # Acts
            predicate = lambda r: r.status_code == 404

            # Assert
            # Checks that the home page does not respond to the predicate and triggers a timeout
            try:
                fixtup.helper.wait_readiness("http://localhost:8888", timeout=10, attempt_every=10, predicate=predicate)
            except TimeoutError as e:
                pass

            fixtup.helper.wait_readiness("http://localhost:8888/missing", timeout=10, attempt_every=10, predicate=predicate)


    def test_wait_readiness_should_trigger_timeout_exception_when_it_is_ellapsed(self):
        # Assign
        # Acts
        try:
            fixtup.helper.wait_readiness("http://localhost:8888", timeout=10, attempt_every=10)
        except TimeoutError as e:
            assert str(e) == "http://localhost:8888 is not ready after 10ms"
        # Assert

if __name__ == '__main__':
    unittest.main()
