from typing import List

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from ..outlets import template_outlets

register = template.Library()

PLUGINOUTLET_SYNTAX_ERROR = 'pluginoutlet tag syntax is "pluginoutlet OUTLET_NAME"'


@register.tag()
def pluginoutlet(_, token):
    split_contents = token.split_contents()
    if len(split_contents) != 2:
        raise template.TemplateSyntaxError(PLUGINOUTLET_SYNTAX_ERROR)

    outlet_name = split_contents[1].strip()
    if not outlet_name:
        raise template.TemplateSyntaxError(PLUGINOUTLET_SYNTAX_ERROR)

    return PluginOutletNode(outlet_name)


class PluginOutletNode(template.Node):
    outlet_name: str

    def __init__(self, outlet_name: str):
        self.outlet_name = outlet_name

    def render(self, context):
        outlet = template_outlets.get(self.outlet_name)
        if not outlet:
            return ""

        request = context.get("request")

        outlet_html = ""
        for plugin_html in outlet(request, context):
            if plugin_html is not None:
                outlet_html += conditional_escape(plugin_html)
        return mark_safe(outlet_html)


HASPLUGINS_SYNTAX_ERROR = 'hasplugins tag syntax is "hasplugins OUTLET_NAME"'


@register.tag()
def hasplugins(parser, token):
    split_contents = token.split_contents()
    if len(split_contents) != 2:
        raise template.TemplateSyntaxError(HASPLUGINS_SYNTAX_ERROR)

    outlet_name = split_contents[1].strip()
    if not outlet_name:
        raise template.TemplateSyntaxError(HASPLUGINS_SYNTAX_ERROR)

    nodelists: List[template.NodeList] = [parser.parse(("else", "endhasplugins"))]
    token = parser.next_token()

    if token.contents == "else":
        nodelists.append(parser.parse(("endhasplugins",)))
        token = parser.next_token()

    if token.contents != "endhasplugins":
        raise template.TemplateSyntaxError(
            'Malformed template tag at line {}: "{}"'.format(
                token.lineno, token.contents
            )
        )

    return HasPluginsNode(outlet_name, nodelists)


class HasPluginsNode(template.Node):
    outlet_name: str
    nodelist: template.NodeList
    nodelist_else: template.NodeList | None

    def __init__(self, outlet_name: str, nodelists: List[template.NodeList]):
        self.outlet_name = outlet_name
        self.nodelist = nodelists[0]

        try:
            self.nodelist_else = nodelists[1]
        except IndexError:
            self.nodelist_else = None

    def render(self, context):
        outlet = template_outlets.get(self.outlet_name)
        if not outlet:
            if self.nodelist_else is not None:
                return self.nodelist_else.render(context)
            return ""

        return self.nodelist.render(context)
