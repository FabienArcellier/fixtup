"""
hack to make mypi not check signal.py file
"""
from typing import Callable

def register_signal_handler(signalnum: int, handler: Callable) -> None:
    pass


def unregister_signal_handler(signalnum: int, handler: Callable) -> None:
    pass
