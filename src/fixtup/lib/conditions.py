from typing import Optional, TypeVar, Callable, Iterable, Any

T = TypeVar('T')  # pylint: disable=invalid-name


def mandatory(_list: Iterable[T], field: Callable[[T], Any]) -> bool:
    """
    check if an attribute is never non in a list

    >>> dashboards = [
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 1'},
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 2'},
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 3'},
    >>> ]
    >>>
    >>> dashboard = mandatory(dashboards, lambda d: d['dashboard'])
    """
    result = True
    for elt in _list:
        value = field(elt)
        if value is None:
            result = False

    return result


def same(_list: Iterable[T], field: Callable[[T], Any]) -> bool:
    """
    checks if all values of an attribute in a list are the same

    >>> dashboards = [
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 1'},
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 2'},
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 3'},
    >>> ]
    >>>
    >>> assert same(dashboards, lambda a: a['user'])
    """
    _original_value = None
    result = True
    for elt in _list:
        value = field(elt)
        if _original_value is None:
            _original_value = value

        if _original_value != value:
            result = False

    return result


def unique(_list: Iterable[T], field: Callable[[T], Any]) -> bool:
    """
    checks if all values of an attribute in a list are unique in the list

    >>> dashboards = [
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 1'},
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 2'},
    >>>    {'user': 'fabien', 'dashboard': 'dashboard 3'},
    >>> ]
    >>>
    >>> assert unique(dashboards, lambda a: a['dashboard'])
    """
    result = True
    values = set()
    for elt in _list:
        value = field(elt)
        if value in values:
            result = False

        values.add(value)

    return result
