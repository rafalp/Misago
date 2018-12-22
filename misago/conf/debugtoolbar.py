import os


def enable_debug_toolbar(_):
    return os.environ.get("IN_MISAGO_DOCKER", "") == "1"
