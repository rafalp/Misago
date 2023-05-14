from django.apps import AppConfig


class MisagoNotificationsConfig(AppConfig):
    name = "misago.notifications"
    label = "misago_notifications"
    verbose_name = "Misago Notifications"

    def ready(self):
        from . import signals as _  # noqa: F401
