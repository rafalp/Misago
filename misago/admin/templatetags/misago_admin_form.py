from django import forms, template

register = template.Library()


@register.inclusion_tag("misago/admin/form/row.html")
def admin_form_row(field, label_class, field_class):
    return {
        "field": field,
        "label_class": label_class,
        "field_class": field_class,
    }


@register.inclusion_tag("misago/admin/form/input.html")
def admin_form_input(field):
    widget_context = field.field.widget.get_context(field.html_name, field.value(), {})

    return {
        "field": field,
        "attrs": widget_context["widget"],
    }


@register.filter
def is_select_field(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def extract_choices_from_attrs(attrs):
    """Filter that extracts field choices into easily iterable list"""
    if attrs.get("optgroups"):
        return [i[1][0] for i in attrs["optgroups"]]
    return []
