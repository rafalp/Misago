from time import time

from django.apps import AppConfig
from django.http import HttpRequest
from misago.context_processors.hooks import get_context_data_hook

from .devwarning import display_dev_warning


class MisagoDevWarningConfig(AppConfig):
    name = "misago_dev_warning"
    verbose_name = "Misago Dev Warning"

    def ready(self):
        get_context_data_hook.append_filter(display_dev_warning)
