import socket

from time import monotonic, sleep

from typing import Optional

__all__ = ['wait_port', 'wait_readiness']


def wait_port(port: int, host: str = 'localhost', timeout: Optional[int] = None, attempt_every: int = 100) -> None:
    """
    wait until a port would be open, for example the port 5432 for postgresql
    before going further

    >>> fixtup.helper.wait_port(5432, timeout=5000)

    :param port: port that has to be open
    :param remote_ip: host on which the port has to be open. It will be localhost by default
    :param timeout: timeout in ms before raising TimeoutError.
    :param attempt_every: time in ms between each attempt to check if the port is responding
    """
    start = monotonic()
    connected = False
    while not connected:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
                connected = True
            except ConnectionRefusedError:
                if timeout is not None and monotonic() - start > (timeout / 1000):
                    raise TimeoutError()

        sleep(attempt_every / 1000)


def wait_readiness(url: str, timeout: Optional[int] = None, attempt_every: int = 100):
    """
    wait until a url reply to http request with 200.

    >>> fixtup.helper.base.wait_readiness(
    >>>         'http://localhost:9000/probes/readz',
    >>>         timeout=5000)

    :param url: port that has to be open
    :param timeout: timeout in ms before raising TimeoutError.
    """
    pass
