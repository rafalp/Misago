from django.apps import AppConfig

from misago.context_processors.hooks import context_processor_hook

from .devwarning import display_dev_warning


class MisagoDevWarningConfig(AppConfig):
    name = "misago_dev_warning"
    verbose_name = "Misago Dev Warning"

    def ready(self):
        context_processor_hook.append_filter(display_dev_warning)
