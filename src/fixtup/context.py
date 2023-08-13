"""
lib_context is a module that manages the global execution context of fixtup. This context is a source of truth shared between all fixtup modules.

It can be retrieved with the ``lib_context()`` function.

>>> from fixtup.context import lib_context
>>> fixtup = lib_context()
"""
from typing import Optional

from fixtup import logger
from fixtup.entity.fixtup import Fixtup

_lib_context: Optional[Fixtup] = None
_fake_lib_context: Optional[Fixtup] = None

def lib_context_setup() -> None:
    """
    Initialize the fixtup context.
    """
    global _lib_context
    if _lib_context is None:
        logger.debug('init a global context for fixtup')
        if _fake_lib_context is None:
            _lib_context = Fixtup()
        else:
            _lib_context = _fake_lib_context
    else:
        logger.debug(f'a global context already exist for fixtup, it reuse it')

def lib_context_teardown() -> None:
    """
    Uninitialize the fixtup context.
    """
    global _lib_context
    _lib_context = None


def lib_context() -> Fixtup:
    """
    returns the context of the fixtup library
    """
    if _lib_context is None:
        """
        If you need to emulate fixtup in automatic testing, you should prepare your test with `with context.use_fake_lib_context()`
        """
        raise RuntimeError("This code must be executed in fixtup lib context.")

    return _lib_context

def lib_context_inject() -> Fixtup:
    """
    Inject a fixtup context. This is useful for testing.
    """
    global _fake_lib_context
    _fake_lib_context = Fixtup()
    return _fake_lib_context

def lib_context_eject() -> None:
    """
    Eject the injected fixtup context. This is useful for testing.

    When tearing down a test, this method cleans up the context that would be loaded when calling `lib_context_setup()`.
    """
    global _fake_lib_context
    _fake_lib_context = None
