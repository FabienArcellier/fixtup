import os


def native_path(path: str) -> str:
    return path.replace('/', os.sep)


def universal_path(path: str) -> str:
    return path.replace(os.sep, '/')


def is_posix() -> bool:
    return os.name == 'posix'


def is_windows() -> bool:
    return os.name == 'nt'
