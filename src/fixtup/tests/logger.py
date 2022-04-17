import contextlib
import logging


@contextlib.contextmanager
def disable_logging(below_level: int = logging.ERROR):
    """
    disable logging for this level and below

    >>> with disable_logging():
    >>>     logging.info("will show nothing, even if the logging level is info")
    >>>     logging.critical("will show something")
    """
    logging.disable(below_level)
    yield
    logging.disable(logging.NOTSET)
