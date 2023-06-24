from typing import Generator, Optional

from contextlib import contextmanager

from fixtup import ctx
from fixtup.entity.fixtup import Fixtup
from fixtup.fixture.factory import reset_fixture_engine


@contextmanager
def use_fake() -> Generator[Fixtup, None, None]:
    """
    replaces the execution context of fixtup with a context that will be configured in the tests
    to be able to test the behavior of fixtup.

    >>> ctx: Fixtup
    >>> with fixture_ctx.use_fake() as ctx:
    >>>     ctx.appdir = '/tmp'
    >>>     # do something in the test
    """
    fake_context = Fixtup()
    current_context = ctx.get()
    try:
        ctx.inject(fake_context)
        yield fake_context
    finally:
        ctx.inject(current_context)


def setup_fake() -> Fixtup:
    """
    replace the execution context of fixtup with a fake context in setUp method and teardown the context
    with tearDown method of unitest.TestCase.

    >>> import unittest
    >>> from fixtures import fixture_ctx
    >>>
    >>> class TestSomething(unittest.TestCase):
    >>>     def setUp(self) -> None:
    >>>         self.context = fixture_ctx.setup_fake()
    >>>
    >>>     def tearDown(self) -> None:
    >>>         fixture_ctx.teardown_fake()
    """
    global _current_context_buffer
    fake_context = Fixtup()
    ctx.inject(fake_context)
    return fake_context


def teardown_fake() -> None:
    """
    replace the execution context of fixtup with a fake context in setUp method and teardown the context
    with tearDown method of unitest.TestCase.

    >>> import unittest
    >>> from fixtures import fixture_ctx
    >>>
    >>> class TestSomething(unittest.TestCase):
    >>>     def setUp(self) -> None:
    >>>         self.context = fixture_ctx.setup_fake()
    >>>
    >>>     def tearDown(self) -> None:
    >>>         fixture_ctx.teardown_fake()
    """
    ctx.inject(None)
    reset_fixture_engine()
