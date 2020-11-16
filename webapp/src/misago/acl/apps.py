from django.apps import AppConfig

from .providers import providers


class MisagoACLsConfig(AppConfig):
    name = "misago.acl"
    label = "misago_acl"
    verbose_name = "Misago ACL framework"

    def ready(self):
        providers.load()
