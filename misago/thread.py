import threading

_thread_local = threading.local()

def local():
    return _thread_local


def clear():
    for attr in _thread_local.__dict__.keys():
        if attr[0] != '_':
            del _thread_local.__dict__[attr]