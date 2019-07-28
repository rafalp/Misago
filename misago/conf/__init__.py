from .static import StaticConf


settings = StaticConf()


def setup(settings_module: str):
    settings.setup(settings_module)
