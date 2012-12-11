from django.conf import settings
from django.utils.importlib import import_module

def build_form(request, form, target):
    return form