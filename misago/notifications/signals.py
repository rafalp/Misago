from django.apps import AppConfig


class MisagoNotificationsConfig(AppConfig):
    name = "misago.notifications"
    label = "misago_notifications"
    verbose_name = "Misago notifications"

    def ready(self):
        from . import signals as _
