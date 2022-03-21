from enum import Enum
from typing import Type, Iterator, TypeVar

T = TypeVar('T', bound=Enum)  # pylint: disable=invalid-name


def enum_values(enum_cls: Type[T]) -> Iterator[T]:
    """
    give an iterator over each value of an enum

    >>> for value in enum_values(HookEvent):
    >>>     print(value)
    """
    for enum in enum_cls:
        yield enum
