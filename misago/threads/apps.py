from django.apps import AppConfig


class MisagoThreadsConfig(AppConfig):
    name = "misago.threads"
    label = "misago_threads"
    verbose_name = "Misago Threads"

    def ready(self):
        from . import signals as _
