import unittest

from fixtup.factory import RuntimeContext, reset_runtime_context, depends, factory


class TestFactory(unittest.TestCase):
    def setUp(self):
        reset_runtime_context()

    def test_depends_use_runtime_context_in_non_unit_test_mode(self):
        # Arrange
        def lookup_parsers(context: RuntimeContext) -> str:
            if context.unittest:
                return "parser a"
            else:
                return "parser b"

        # Acts
        parser = depends(lookup_parsers)

        # Assert
        self.assertEqual("parser b", parser)

    def test_depends_use_runtime_context_in_unit_test_mode(self):
        # Arrange
        reset_runtime_context(RuntimeContext(unittest=True))

        def lookup_parsers(context: RuntimeContext) -> str:
            if context.unittest:
                return "parser a"
            else:
                return "parser b"

        # Acts
        parser = depends(lookup_parsers)

        # Assert
        self.assertEqual("parser a", parser)

    def test_factory_wrap_method_and_inject_runtime_context_in_unit_test_mode(self):
        # Arrange
        reset_runtime_context(RuntimeContext(unittest=True))

        @factory
        def lookup_parsers(context: RuntimeContext) -> str:
            if context.unittest:
                return "parser a"
            else:
                return "parser b"

        # Acts
        parser = lookup_parsers()

        # Assert
        self.assertEqual("parser a", parser)


if __name__ == '__main__':
    unittest.main()
