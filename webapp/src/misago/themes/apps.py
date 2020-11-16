from django.apps import AppConfig


class MisagoThemesConfig(AppConfig):
    name = "misago.themes"
    label = "misago_themes"
    verbose_name = "Misago Theming"

    def ready(self):
        # pylint: disable=unused-import
        from .admin import tasks
