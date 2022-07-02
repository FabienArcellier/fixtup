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


@contextmanager
def with_cwd(directory: str):
    """
    override the current folder

    In case the current folder does not exist, it keeps at the end of the execution the folder
    which has been configured as the new current folder

    If the new current folder does not exist, nothing happens.
    """
    try:
        previous_cwd = os.getcwd()
    except FileNotFoundError:
        previous_cwd = directory

    if os.path.isdir(directory):
        try:
            os.chdir(directory)
            yield
        finally:
            os.chdir(previous_cwd)
    else:
        yield
