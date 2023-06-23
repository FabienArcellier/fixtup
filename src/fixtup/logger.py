from typing import Optional

import logging

DEFAULT_LOGGER = 'fixtup'

def warning(*args, name: str = None, **kwargs) -> None:
    """
    log a warning message. It use the same signature as `Logger.warning``.

    >>> logger.warning("this is a warning message")
    >>> logger.warning("this is a warning message", name="customlogger")
    """
    logger = get_logger(name)
    logger.warning(*args, **kwargs)


def info(*args, name: str = None, **kwargs) -> None:
    """
    log a info message. It use the same signature as `Logger.info``.

    >>> logger.info("this is an info message")
    >>> logger.info("this is an info message", name="customlogger")
    """
    logger = get_logger(name)
    logger.info(*args, **kwargs)


def debug(*args, name: str = None, **kwargs) -> None:
    """
    log a debug message. It use the same signature as `Logger.debug``.

    >>> logger.debug("this is a debug message")
    >>> logger.debug("this is a debug message", name="customlogger")
    """
    logger = get_logger(name)
    logger.debug(*args, **kwargs)


def error(*args, name: str = None, **kwargs) -> None:
    """
    log a error message. It use the same signature as `Logger.error``.

    >>> logger.error("this is an error message")
    >>> logger.error("this is an error message", name="customlogger")
    """
    logger = get_logger(name)
    logger.error(*args, **kwargs)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name is None:
        name = DEFAULT_LOGGER

    logger = logging.getLogger(name)
    return logger



