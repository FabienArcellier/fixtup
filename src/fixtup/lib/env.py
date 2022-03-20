import os
from contextlib import contextmanager


@contextmanager
def env_override(overrides: dict):
    previous_values = {}
    for variable, value in overrides.items():
        if variable in os.environ:
            previous_values[variable] = os.environ[variable]

        os.environ[variable] = value

    yield

    for variable, _ in overrides.items():
        if variable in previous_values:
            os.environ[variable] = previous_values[variable]
        else:
            del os.environ[variable]
