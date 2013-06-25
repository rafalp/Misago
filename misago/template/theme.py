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
    print _thread_local.__dict__.keys()
    _thread_local.misago_theme = theme;
    _thread_local.misago_template_mutex = False


def active_theme():
    try:
        return _thread_local.misago_theme
    except AttributeError:
        return None


def prefix_templates(templates, dictionary=None):
    templates = process_templates(templates, dictionary)
    if isinstance(templates, str):
        return ('%s/%s' % (_thread_local.misago_theme, templates), templates)
    else:
        prefixed = []
        for template in templates:
            prefixed.append('%s/%s' % (_thread_local.misago_theme, template))
        prefixed += templates
        return tuple(prefixed)
