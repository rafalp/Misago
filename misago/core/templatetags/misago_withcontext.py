from django import template

register = template.Library()


@register.tag("withcontext")
def withcontext(parser, token):
    args = token.split_contents()[:]
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "%r requires at least one argument" % args[0]
        )

    nodelist = parser.parse(("endwithcontext",))
    parser.delete_first_token()
    return WithContextNode(nodelist, args[1:])


class WithContextNode(template.Node):
    def __init__(self, nodelist, values):
        self.nodelist = nodelist
        self.values = values

    def __repr__(self):
        return "<%s>" % self.__class__.__name__

    def render(self, context):
        extra_context = {}
        for value in self.values:
            if value_context := context.get(value):
                extra_context.update(value_context)

        with context.push(**extra_context):
            return self.nodelist.render(context)
