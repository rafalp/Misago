from django.apps import AppConfig


class MisagoLegalConfig(AppConfig):
    name = "misago.legal"
    label = "misago_legal"
    verbose_name = "Misago Legal"

    def ready(self):
        from . import signals as _
