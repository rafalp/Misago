from django.apps import AppConfig


class MisagoForumsConfig(AppConfig):
    name = 'misago.forums'
    label = 'misago_forums'
    verbose_name = "Misago Forums"

    def ready(self):
        from misago.forums import signals
