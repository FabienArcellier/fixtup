from typing import Generator, Optional

from contextlib import contextmanager

from fixtup import context
from fixtup.entity.context import Context
from fixtup.fixture.factory import fixture_engine_down


@contextmanager
def use_fake() -> Generator[Context, None, None]:
    """
    replaces the execution context of fixtup with a context that will be configured in the tests
    to be able to test the behavior of fixtup.

    >>> ctx: Context
    >>> with fixture_context.use_fake() as ctx:
    >>>     ctx.appdir = '/tmp'
    >>>     # do something in the test
    """
    fake_context = Context()
    current_context = context.current()
    try:
        context.inject(fake_context)
        yield fake_context
    finally:
        context.inject(current_context)


def setup_fake() -> Context:
    """
    replace the execution context of fixtup with a fake context in setUp method and teardown the context
    with tearDown method of unitest.TestCase.

    >>> import unittest
    >>> from fixtures import fixture_context
    >>>
    >>> class TestSomething(unittest.TestCase):
    >>>     def setUp(self) -> None:
    >>>         self.context = fixture_context.setup_fake()
    >>>
    >>>     def tearDown(self) -> None:
    >>>         fixture_context.teardown_fake()
    """
    global _current_context_buffer
    fake_context = Context()
    context.inject(fake_context)
    return fake_context


def teardown_fake() -> None:
    """
    replace the execution context of fixtup with a fake context in setUp method and teardown the context
    with tearDown method of unitest.TestCase.

    >>> import unittest
    >>> from fixtures import fixture_context
    >>>
    >>> class TestSomething(unittest.TestCase):
    >>>     def setUp(self) -> None:
    >>>         self.context = fixture_context.setup_fake()
    >>>
    >>>     def tearDown(self) -> None:
    >>>         fixture_context.teardown_fake()
    """
    context.inject(None)
    fixture_engine_down()
