#!/usr/bin/env python
import os

from misago import setup
from misago.conf import settings


if __name__ == "__main__":
    os.environ.setdefault("MISAGO_SETTINGS_MODULE", "app.settings")

    setup()
    print("HELLO", settings.INSTALLED_PLUGINS)