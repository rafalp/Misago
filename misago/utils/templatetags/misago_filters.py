from django import template
from django.template.defaultfilters import stringfilter
from misago.utils import slugify

register = template.Library()

@register.filter(name="slugify", is_safe=True)
@stringfilter
def slugify_tag(format_string):
    return slugify(format_string)

@register.filter(name='klass', is_safe=True)
def class_tag(obj):
    return obj.__class__.__name__