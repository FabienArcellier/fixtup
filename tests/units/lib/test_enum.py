import unittest

from fixtup.lib.enum import Enum, enum_values


class DummyEnum(Enum):
    value1 = "value1"
    value2 = "value2"


class TestEnum(unittest.TestCase):

    def test_enum_values_should_return_a_list_of_options(self):
        # Arrange
        # Acts
        result = enum_values(DummyEnum)

        # Assert
        self.assertEqual([DummyEnum.value1, DummyEnum.value2], list(result))


if __name__ == '__main__':
    unittest.main()
