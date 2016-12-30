from .conf import OLD_FORUM
from .db import fetch_assoc


class DevNull(object):
    def write(self, *args, **kwargs):
        pass
defstdout = DevNull()
