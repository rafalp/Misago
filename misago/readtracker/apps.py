from django.apps import AppConfig


class MisagoReadTrackerConfig(AppConfig):
    name = 'misago.readtracker'
    label = 'misago_readtracker'
    verbose_name = "Misago Read Tracker"

    def ready(self):
        from . import signals as _
