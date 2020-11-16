from django.apps import AppConfig


class MisagoSSOConfig(AppConfig):
    """
    Using https://github.com/divio/django-simple-sso
    """

    name = "misago.sso"
    label = "misago_sso"
    verbose_name = "Misago Single Sign On"
