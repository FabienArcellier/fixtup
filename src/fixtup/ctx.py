from typing import Optional

from fixtup import logger
from fixtup.entity.fixtup import Fixtup

_ctx: Optional[Fixtup] = None


def get() -> Fixtup:
    """
    returns the context of the fixtup library
    """
    if _ctx is None:
        """
        If you need to emulate fixtup in automatic testing, you should prepare your test with `with ctx_fixture.mock()`.
        """
        raise RuntimeError("This code must be executed in a fixtup context.")

    return _ctx


def start() -> Fixtup:
    """
    Le context démarre la première fois que cette fonction est appellée ou si un context
    :return:
    """
    global _ctx
    if _ctx is None:
        logger.debug('init a global context for fixtup')
        _ctx = Fixtup()
    else:
        logger.debug(f'a global context already exist for fixtup, it reuse it')

    return _ctx


def inject(context: Optional[Fixtup]):
    """
    this function allows the fixture fixture_ctx.use_fake to override the fixtup context.

    This function is dedicated to the automatic test.
    """
    global _ctx
    _ctx = context
