from django.shortcuts import (redirect, render as django_render,
                              render_to_response as django_render_to_response)
from misago.template.middlewares import process_context
from misago.template.theme import prefix_templates
from misago.utils.views import redirect_message, json_response

def render(request, template_name, dictionary=None, **kwargs):
    dictionary = process_context(template_name, dictionary, kwargs.pop('context_instance', None))
    template_name = prefix_templates(template_name, dictionary)
    return django_render(request, template_name, dictionary, **kwargs)


def render_to_response(template_name, dictionary=None, **kwargs):
    dictionary = process_context(template_name, dictionary, kwargs.get('context_instance'))
    template_name = prefix_templates(template_name, dictionary)
    return django_render_to_response(template_name, dictionary, content_type=kwargs.get('content_type'))
