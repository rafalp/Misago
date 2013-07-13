from markdown import markdown
from django_jinja.library import Library
from django.conf import settings
import misago.markdown

register = Library()


@register.filter(name='markdown')
def parse_markdown(value, format=None):
    if not format:
        format = settings.OUTPUT_FORMAT
    return markdown(value,
                    safe_mode='escape',
                    output_format=format,
                    extensions=['nl2br', 'fenced_code']).strip()


@register.filter(name='markdown_short')
def short_markdown(value, length=300):
    value = misago.markdown.clear_markdown(value)

    if len(value) <= length:
        return ' '.join(value.splitlines())

    value = ' '.join(value.splitlines())
    value = value[0:length]

    while value[-1] != ' ':
        value = value[0:-1]

    value = value.strip()
    if value[-3:3] != '...':
        value = '%s...' % value

    return value


@register.filter(name='markdown_final')
def finalize_markdown(value):
    return misago.markdown.finalize_markdown(value)