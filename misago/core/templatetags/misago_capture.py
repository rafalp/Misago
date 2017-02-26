"""
Capture tag: renders its contents as template, and stores them in value

Syntax:
{% capture trimmed as loremipsum %}
<a href="{% url 'misago:terms-of-service' %}">{% trans "guidelines" %}</a>
{% endcapture %} # renders block contents to context variable loremipsum
"""

from django import template


register = template.Library()
SYNTAX_ERROR = 'capture tag syntax is "capture [trimmed] as [value]"'


@register.tag()
def capture(parser, token):
    split_contents = token.split_contents()

    if len(split_contents) == 4:
        if split_contents[1] != 'trimmed' or split_contents[2].lower() != 'as':
            raise template.TemplateSyntaxError(SYNTAX_ERROR)
        is_trimmed = True
        variable = split_contents[3]
    elif len(split_contents) == 3:
        if split_contents[1].lower() != 'as':
            raise template.TemplateSyntaxError(SYNTAX_ERROR)
        is_trimmed = False
        variable = split_contents[2]
    else:
        raise template.TemplateSyntaxError(SYNTAX_ERROR)

    nodelist = parser.parse(('endcapture', ))
    parser.delete_first_token()
    return CaptureNode(variable, nodelist, trim=is_trimmed)


class CaptureNode(template.Node):
    def __init__(self, variable, nodelist, trim=False):
        self.variable = variable
        self.nodelist = nodelist
        self.is_trimmed = trim

    def render(self, context):
        captured_output = self.nodelist.render(context)
        if self.is_trimmed:
            captured_output = captured_output.strip()
        context[self.variable] = captured_output
        return ''
