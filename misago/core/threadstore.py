from threading import local


_thread_local = local()


def get(key, default=None):
    return _thread_local.__dict__.get(key, default)


def set(key, value):
    return _thread_local.__dict__[key] = value


def clear():
    _thread_local.__dict__ = {}
