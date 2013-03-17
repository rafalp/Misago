from django.conf import settings
from coffin.shortcuts import render, render_to_response
from coffin.template.loader import get_template, select_template, render_to_string

'''Monkeypatch Django to mimic Jinja2 behaviour'''
from django.utils import safestring
if not hasattr(safestring, '__html__'):
    safestring.SafeString.__html__ = lambda self: str(self)
    safestring.SafeUnicode.__html__ = lambda self: unicode(self)

class Theme(object):
    def __init__(self, theme):
        self.set_theme(theme);

    def set_theme(self, theme):
        if theme not in settings.INSTALLED_THEMES:
            raise ValueError('"%s" is not correct theme name.' % theme)
        if theme[0] == '_':
            raise ValueError('"%s" is a template package, not a theme.' % theme[1:])
        self._theme = theme;

    def reset_theme(self):
        self._theme = settings.INSTALLED_THEMES[0]

    def get_theme(self):
        return self._theme

    def prefix_templates(self, templates):
        if isinstance(templates, str):
            return ('%s/%s' % (self._theme, templates), templates)
        else:
            prefixed = []
            for template in templates:
                prefixed.append('%s/%s' % (self._theme, template))
            prefixed += templates
            return prefixed

    def render(self, request, *args, **kwargs):
        return render(request, *args, **kwargs)

    def render_to_string(self, templates, *args, **kwargs):
        templates = self.prefix_templates(templates)
        return render_to_string(templates, *args, **kwargs)

    def render_to_response(self, templates, *args, **kwargs):
        templates = self.prefix_templates(templates)
        return render_to_response(templates, *args, **kwargs)

    def get_email_templates(self, template, contex={}):
            email_type_plain = '_email/%s_plain.html' % template
            email_type_html = '_email/%s_html.html' % template
            return (
                    select_template(('%s/%s' % (self._theme, email_type_plain[1:]), email_type_plain)),
                    select_template(('%s/%s' % (self._theme, email_type_html[1:]), email_type_html)),
                    )
