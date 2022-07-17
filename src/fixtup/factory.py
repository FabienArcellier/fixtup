"""
This module implements the inversion of control mechanism.

It allows to instantiate factory methods
which take advantage of the runtime configuration to infer
the dependencies to be instantiated.

If the code is used in unit tests, it is possible
instantiate specific dependencies.
"""
import threading
from typing import Optional, Callable, TypeVar, Any

import attr

T = TypeVar('T')


@attr.s
class RuntimeContext:
    """
    The runtime context describes the conditions of the runtime is executed.
    By default, RuntimeContext match production context
    """
    unittest = attr.ib(default=False)

    """
    The plugins are ignored when enable_plugins is False.

    They are not loaded, neither executed. The plugin engine is doing
    pass-through
    """
    enable_plugins = attr.ib(default=True)

    """
<<<<<<< HEAD
    The hooks are ignored when enable_hooks is False.

    They are not loaded, neither executed. The plugin engine is doing
    pass-through
    """
    enable_hooks = attr.ib(default=True)

    """
    When we use 2 successive fixtures in a test and this flag is active,
    we consider that the 2 fixtures are executed in separate test processes.

    This flag is essential internally to test the behavior of policies such as keep_up, ...
    """
    emulate_new_process = attr.ib(default=False)


"""
Using threading store allow to perform dependency injection in
a multithreading context.

Automatic test may be run in parallel, we want avoid concurrent test
share a same runtime context
"""
thread_store = threading.local()
thread_store.runtime_conf = RuntimeContext()


def reset_runtime_context(context: Optional[RuntimeContext] = None):
    if context is None:
        thread_store.runtime_conf = RuntimeContext()
    else:
        thread_store.runtime_conf = context


def depends(func: Callable[..., T], *args, **kwargs) -> T:
    """
    this method allow to manage binding rules to tune the behavior depending of runtime option.
    If we execute a code during unittest, we want to inject specific dependency

    :param func:

    >>> def lookup_parsers(context: RuntimeContext) -> str:
    >>>     if context.unittest:
    >>>         return "parser a"
    >>>     else:
    >>>         return "parser b"
    >>>
    >>> parser = depends(lookup_parsers)
    >>> print(parser)
    """

    return func(thread_store.runtime_conf, *args, **kwargs)


def factory(func: Callable[['RuntimeContext'], T]) -> Callable[..., T]:
    """
    build factory method. The runtime context will be injected from the thread store.

    >>> @factory
    >>> def lookup_parsers(context: RuntimeContext) -> str:
    >>>     if context.unittest:
    >>>         return "parser a"
    >>>     else:
    >>>         return "parser b"
    >>>
    >>> parser = lookup_parsers()
    >>> print(parser)

    :param func:
    """

    def _wrapper(*args, **kwargs) -> T:
        return depends(func, *args, **kwargs)

    return _wrapper
