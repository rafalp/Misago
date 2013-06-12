from django.conf import settings
from django.utils.importlib import import_module
from coffin.shortcuts import render_to_response
from coffin.template import dict_from_django_context
from coffin.template.loader import get_template, select_template, render_to_string

'''Monkeypatch Django to mimic Jinja2 behaviour'''
from django.utils import safestring
if not hasattr(safestring, '__html__'):
    safestring.SafeString.__html__ = lambda self: str(self)
    safestring.SafeUnicode.__html__ = lambda self: unicode(self)

class Theme(object):
    middlewares = ()

    def __init__(self, theme):
        self.set_theme(theme);

        if not self.middlewares:
            self.load_middlewares(settings.TEMPLATE_MIDDLEWARES)

    def load_middlewares(self, middlewares):
        for extension in middlewares:
            module = '.'.join(extension.split('.')[:-1])
            extension = extension.split('.')[-1]
            module = import_module(module)
            middleware = getattr(module, extension)
            self.middlewares += (middleware(), )

    def merge_contexts(self, dictionary=None, context_instance=None):
        dictionary = dictionary or {}
        if context_instance:
            context_instance.update(dictionary)
        else:
            context_instance = dictionary
        return context_instance

    def process_context(self, templates, context):
        for middleware in self.middlewares:
            try:
                new_context = middleware.process_context(self, templates, context)
                if new_context:
                    context = new_context
            except AttributeError:
                pass
        return context

    def process_template(self, templates, context):
        for middleware in self.middlewares:
            try:
                new_templates = middleware.process_template(self, templates, context)
                if new_templates:
                    return new_templates
            except AttributeError:
                pass
        return templates

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

    def prefix_templates(self, templates, dictionary=None):
        templates = self.process_template(templates, dictionary)
        if isinstance(templates, str):
            return ('%s/%s' % (self._theme, templates), templates)
        else:
            prefixed = []
            for template in templates:
                prefixed.append('%s/%s' % (self._theme, template))
            prefixed += templates
            return prefixed

    def render_to_string(self, templates, dictionary=None, context_instance=None):
        dictionary = self.process_context(templates, self.merge_contexts(dictionary, context_instance))
        templates = self.prefix_templates(templates, dictionary)
        return render_to_string(templates, dictionary)

    def render_to_response(self, templates, dictionary=None, context_instance=None,
                       mimetype=None):
        dictionary = self.process_context(templates, self.merge_contexts(dictionary, context_instance))
        templates = self.prefix_templates(templates, dictionary)
        return render_to_response(templates, dictionary=dictionary, mimetype=mimetype)

    def macro(self, templates, macro, dictionary={}, context_instance=None):
        templates = self.prefix_templates(templates, dictionary)
        template = select_template(templates)
        if context_instance:
            context_instance.update(dictionary)
        else:
            context_instance = dictionary
        context_instance = dict_from_django_context(context_instance)
        _macro = getattr(template.make_module(context_instance), macro)
        return unicode(_macro()).strip()

    def get_email_templates(self, template, contex={}):
            email_type_plain = '_email/%s.txt' % template
            email_type_html = '_email/%s.html' % template
            return (
                    select_template(('%s/%s' % (self._theme, email_type_plain[1:]), email_type_plain)),
                    select_template(('%s/%s' % (self._theme, email_type_html[1:]), email_type_html)),
                    )
