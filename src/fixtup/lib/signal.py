import signal
from typing import Callable, Optional, List


class SignalHandlers():

    def __init__(self, orignal_handler: Optional[Callable]):
        self.handlers : List[Callable] = []
        self.orignal_handler = orignal_handler

    def register(self, handler: Callable):
        self.handlers.append(handler)

    def unregister(self, handler: Callable):
        self.handlers.remove(handler)

    def __call__(self, signum: int, frame):
        for handler in self.handlers:
            handler(signum, frame)

        if self.orignal_handler is not None:
            self.orignal_handler(signum, frame)


def register_signal_handler(signalnum: int, handler: Callable) -> None:
    _handler = signal.getsignal(signalnum)
    if isinstance(handler, SignalHandlers):
        _handler.register(handler)
    else:
        new_handler = SignalHandlers(_handler)
        new_handler.register(handler)
        signal.signal(signalnum, new_handler)


def unregister_signal_handler(signalnum: int, handler: Callable) -> None:
    _handler = signal.getsignal(signalnum)
    if not isinstance(_handler, SignalHandlers):
        raise ValueError('you can apply unregister_signal_handler after register_signal_handler')

    _handler.unregister(handler)
