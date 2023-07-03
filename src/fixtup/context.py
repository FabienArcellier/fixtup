"""
Initializes a context for the fixtup library, freely accessible through ``context.current()``.

This context is initialized when fixtup is started, either when starting the first fixture or when executing a command.

>>> from fixtup import context
>>> ctx = context.current()
"""
from typing import Optional

from fixtup import logger
from fixtup.entity.context import Context
from fixtup.fixture.factory import fixture_engine_down

_context: Optional[Context] = None


def current() -> Context:
    """
    returns the context of the fixtup library
    """
    if _context is None:
        """
        If you need to emulate fixtup in automatic testing, you should prepare your test with `with ctx_fixture.mock()`.
        """
        raise RuntimeError("This code must be executed in a fixtup context.")

    return _context


def up() -> Context:
    """
    Mount the fixtup context.
    """
    global _context
    if _context is None:
        logger.debug('init a global context for fixtup')
        _context = Context()
    else:
        logger.debug(f'a global context already exist for fixtup, it reuse it')

    return _context


def inject(context: Optional[Context]):
    """
    this function allows the fixture fixture_ctx.use_fake to override the fixtup context.

    This function is dedicated to the automatic test.
    """
    global _context
    _context = context


def down() -> None:
    global _context
    _context = None
    fixture_engine_down()
