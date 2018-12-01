from threading import local


_thread_local = local()


def get(key, default=None):
    return default


def set(key, value):
    return value


def clear():
    pass
