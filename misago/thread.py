import threading

_thread_local = threading.local()

def local():
    return _thread_local
