from django.conf import settings
from django.core.checks import register, Critical


@register()
def db_check(app_configs, **kwargs):
    errors = []

    try:
        supported_driver = 'django.db.backends.postgresql_psycopg2'
        if settings.DATABASES['default']['ENGINE'] != supported_driver:
            raise ValueError()
    except (AttributeError, KeyError, ValueError):
        errors.append(Critical(msg='Misago requires PostgreSQL database.',
                               id='misago.001'))

    return errors


default_app_config = 'misago.core.apps.MisagoCoreConfig'
