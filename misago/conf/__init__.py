from .gateway import settings, db_settings  # noqa

default_app_config = 'misago.conf.apps.MisagoConfConfig'

SETTINGS_CACHE = "settings"

# Feature flag for easy changing between old and new settings mechanism
ENABLE_GLOBAL_STATE = True  # FIXME: delete after API changes
