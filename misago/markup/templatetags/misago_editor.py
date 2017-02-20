from django import template
from django.template import Context
from django.template.loader import get_template


register = template.Library()


def _render_editor_template(context, editor, tpl):
    c = Context(context)
    c['editor'] = editor

    return get_template(tpl).render(c)


def editor_body(context, editor):
    return _render_editor_template(context, editor, editor.body_template)


register.simple_tag(takes_context=True)(editor_body)


def editor_js(context, editor):
    return _render_editor_template(context, editor, editor.js_template)


register.simple_tag(takes_context=True)(editor_js)
