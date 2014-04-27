from django.conf import settings
from django.shortcuts import render as dj_render
from misago.admin import site


def get_admin_namespace(requested_namespace):
    for namespace in settings.MISAGO_ADMIN_NAMESPACES:
        if requested_namespace[:len(namespace)] == namespace:
            return namespace
    else:
        return None


def render(request, template, context=None):
    context = context or {}

    navigation = site.visible_branches(request)
    sections = navigation[0]

    try:
        actions = navigation[1]
    except IndexError:
        actions = []

    try:
        pages = navigation[2]
    except IndexError:
        pages = []

    context.update({
            'sections': sections,
            'actions': actions,
            'pages': pages
        })

    return dj_render(request, template, context)
