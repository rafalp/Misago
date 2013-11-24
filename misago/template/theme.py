from django.conf import settings
from misago.template.middlewares import process_templates
from misago.thread import local

__all__ = ('activate_theme', 'active_theme', 'prefix_templates')

_thread_local = local()

def activate_theme(theme):
    """
    Activate theme in current thread
    """
    if theme not in settings.INSTALLED_THEMES:
        raise ValueError('"%s" is not correct theme name.' % theme)
    if theme[0] == '_':
        raise ValueError('"%s" is a template package, not a theme.' % theme[1:])
    
    _thread_local.theme = theme;
    _thread_local.template_mutex = False


def reset_theme():
    _thread_local.theme = settings.INSTALLED_THEMES[0];


def active_theme():
    try:
        return _thread_local.theme
    except AttributeError:
        return None


def prefix_templates(templates, dictionary=None):
    templates = process_templates(templates, dictionary)
    if isinstance(templates, str):
        return ('%s/%s' % (_thread_local.theme, templates), templates)
    else:
        prefixed = []
        for template in templates:
            prefixed.append('%s/%s' % (_thread_local.theme, template))
        prefixed += templates
        return tuple(prefixed)
