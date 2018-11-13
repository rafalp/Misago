from django import forms, template
from django.template.loader import render_to_string

register = template.Library()


@register.tag
def form_row(parser, token):
    """
    Form row: renders single row in form

    Syntax:
    {% form_row form.field %} # renders vertical field
    {% form_row form.field "col-md-3" "col-md-9" %} # renders horizontal field
    """
    args = token.split_contents()

    if len(args) < 2:
        raise template.TemplateSyntaxError("form_row tag requires at least one argument")

    if len(args) == 3 or len(args) > 4:
        raise template.TemplateSyntaxError(
            "form_row tag supports either one argument (form field) or "
            "four arguments (form field, label class, field class)"
        )

    form_field = args[1]

    if len(args) == 4:
        label_class = args[2]
        field_class = args[3]
    else:
        label_class = None
        field_class = None

    return FormRowNode(form_field, label_class, field_class)


class FormRowNode(template.Node):
    def __init__(self, form_field, label_class, field_class):
        self.form_field = template.Variable(form_field)

        if label_class and field_class:
            self.label_class = template.Variable(label_class)
            self.field_class = template.Variable(field_class)
        else:
            self.label_class = None
            self.field_class = None

    def render(self, context):
        field = self.form_field.resolve(context)

        if self.label_class and self.field_class:
            label_class = self.label_class.resolve(context)
            field_class = self.field_class.resolve(context)
        else:
            label_class = None
            field_class = None

        return render_to_string(
            'misago/admin/forms/row.html', {
                'field': field,
                'label_class': label_class or '',
                'field_class': field_class or '',
            }
        )


@register.simple_tag
def form_field(*args):
    """form input: renders given field input"""
    return "TODO"


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_checkboxselectmultiple(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radioselect(field):
    return isinstance(field.field.widget, forms.RadioSelect)
