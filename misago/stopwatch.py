import time

class Stopwatch(object):
    def __init__(self):
        self.start_time = time.time()
    def time(self):
        return time.time() - self.start_time 