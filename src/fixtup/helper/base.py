import socket

from time import monotonic, sleep

from typing import Optional, Callable

import requests
from requests import Response

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


def wait_readiness(url: str, timeout: Optional[int] = None, attempt_every: int = 1000, predicate: Optional[Callable[[Response], bool]] = None) -> None:
    """
    wait until a url reply to http request with 200.

    >>> fixtup.helper.base.wait_readiness(
    >>>         'http://localhost:9000/probes/readz',
    >>>         timeout=5000)

    :param url: port that has to be open
    :param timeout: timeout in ms before raising TimeoutError.
    :param attempt_every: time in ms between each attempt to check if the port is responding (default 1000ms)
    :param predicate: a function that takes the request response and check if the result is valid
    """
    start = monotonic()
    ready = False
    while ready is False and (timeout is None or monotonic() - start < timeout / 1000):
        try:
            r = requests.get(url)
            if predicate is None:
                predicate = lambda r: r.status_code == 200

            if predicate(r):
                ready = True
                break
                
        except requests.exceptions.ConnectionError:
            pass

        sleep(attempt_every / 1000)

    if ready is False:
        raise TimeoutError(f"{url} is not ready after {timeout}ms")

    return
