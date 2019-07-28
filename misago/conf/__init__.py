import os

from .static import StaticConf


conf = StaticConf()


def configure(settings_module: str):
    conf.configure(settings_module or os.environ.get('MISAGO_SETTINGS_MODULE'))
