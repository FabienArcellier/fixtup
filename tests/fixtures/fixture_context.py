from typing import Generator, Optional

from contextlib import contextmanager

from fixtup.context import lib_context_setup, lib_context_teardown, lib_context
from fixtup.entity.fixtup import Fixtup


@contextmanager
def use_lib_context() -> Generator[Fixtup, None, None]:
    """
    replaces the execution context of fixtup with a context that will be configured in the tests
    to be able to test the behavior of fixtup.

    >>> ctx: Context
    >>> with fixture_context.use_lib_context() as ctx:
    >>>     ctx.appdir = '/tmp'
    >>>     # do something in the test
    """
    try:
        lib_context_setup()
        yield lib_context()
    finally:
        lib_context_teardown()
