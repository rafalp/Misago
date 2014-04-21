from django.conf import settings
from django.shortcuts import render as dj_render


def get_admin_namespace(requested_namespace):
    for namespace in settings.MISAGO_ADMIN_NAMESPACES:
        if requested_namespace[:len(namespace)] == namespace:
            return namespace
    else:
        return None


def render(request, template, context=None):
    context = context or {}

    return dj_render(request, template, context)
