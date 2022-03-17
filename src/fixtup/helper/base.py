from typing import Optional

__all__ = ['wait_port', 'wait_readiness']


def wait_port(port: int, host: str = 'localhost', timeout: Optional[int] = None):
    """
    wait until a port would be open, for example the port 5432 for postgresql
    before going further

    >>> fixtup.helper.base.wait_port(5432, timeout=5000)

    :param port: port that has to be open
    :param remote_ip: host on which the port has to be open. It will be localhost by default
    :param timeout: timeout in ms before raising TimeoutError.
    """
    pass


def wait_readiness(url: str, timeout: Optional[int] = None):
    """
    wait until a url reply to http request with 200.

    >>> fixtup.helper.base.wait_readiness(
    >>>         'http://localhost:9000/probes/readz',
    >>>         timeout=5000)

    :param url: port that has to be open
    :param timeout: timeout in ms before raising TimeoutError.
    """
    pass
