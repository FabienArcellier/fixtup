from typing import TypeVar, Iterable, Callable, Optional

T = TypeVar('T')  # pylint: disable=invalid-name


def first(_list: Iterable[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """
    return the first element of the list if it match the predicate, otherwise it returns None
    """
    result = None
    for elt in _list:
        if predicate(elt):
            result = elt
            break

    return result

