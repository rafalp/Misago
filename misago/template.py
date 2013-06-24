import threading
from django.conf import settings
from django.shortcuts import (render as django_render,
                              render_to_response as django_render_to_response)
from django.template import RequestContext
from django.template.loader import render_to_string as django_render_to_string
from django.utils.importlib import import_module

_thread_local = threading.local()

def activate_theme(theme):
    if theme not in settings.INSTALLED_THEMES:
        raise ValueError('"%s" is not correct theme name.' % theme)
    if theme[0] == '_':
        raise ValueError('"%s" is a template package, not a theme.' % theme[1:])
    _thread_local.misago_theme = theme;


def theme_name():
    try:
        return _thread_local.misago_theme
    except AttributeError:
        return None


def render(*args, **kwargs):
    return django_render(*args, **kwargs)


def render_to_string(*args, **kwargs):
    return django_render_to_string(*args, **kwargs)


def render_to_response(*args, **kwargs):
    return django_render_to_response(*args, **kwargs)