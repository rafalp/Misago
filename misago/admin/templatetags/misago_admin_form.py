from django import forms, template
from django.utils.html import format_html_join

from ..forms import YesNoSwitchBase

register = template.Library()


@register.inclusion_tag("misago/admin/form/row.html")
def form_row(field, label_class=None, field_class=None):
    return {"field": field, "label_class": label_class, "field_class": field_class}


@register.inclusion_tag("misago/admin/form/image_row.html")
def form_image_row(
    field,
    label_class=None,
    field_class=None,
    image_class=None,
    delete_field=None,
    size=None,
    dimensions=None,
):
    return {
        "field": field,
        "field_image": field.initial,
        "size": size,
        "dimensions": get_field_image_dimensions(dimensions),
        "delete_field": delete_field,
        "label_class": label_class,
        "field_class": field_class,
        "image_class": image_class,
    }


def get_field_image_dimensions(dimensions):
    if dimensions:
        return {"width": dimensions[0], "height": dimensions[1]}
    return None


@register.inclusion_tag("misago/admin/form/checkbox_row.html")
def form_checkbox_row(field, label_class=None, field_class=None):
    return {"field": field, "label_class": label_class, "field_class": field_class}


@register.inclusion_tag("misago/admin/form/input.html")
def form_input(field):
    attrs = field.field.widget.attrs
    context = field.field.widget.get_context(field.html_name, field.value(), attrs)
    context["attrs"] = attrs
    context["field"] = field
    return context


@register.simple_tag
def render_attrs(widget, class_name=None):
    rendered_attrs = []
    for attr, value in widget["attrs"].items():
        if value not in (True, False, None):
            rendered_attrs.append((attr, value))
    if not widget["attrs"].get("class") and class_name:
        rendered_attrs.append(("class", class_name))
    return format_html_join(" ", '{}="{}"', rendered_attrs)


@register.simple_tag
def render_bool_attrs(widget):
    attrs_html = []
    for attr, value in widget.items():
        if value is True:
            attrs_html.append(attr)
    return " ".join(attrs_html)


@register.filter
def is_yesno_switch_field(field):
    return isinstance(field.field, YesNoSwitchBase)


@register.filter
def is_radio_select_field(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_select_field(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_multiple_choice_field(field):
    multichoice_widgets = (forms.CheckboxSelectMultiple, forms.SelectMultiple)
    return isinstance(field.field.widget, multichoice_widgets)


@register.filter
def is_textarea_field(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def get_options(field):
    """Filter that extracts field choices into an easily iterable list"""
    widget = field.field.widget
    attrs = dict(id=field.auto_id, **widget.attrs)
    context = widget.get_context(field.html_name, field.value(), attrs)
    widget_context = context["widget"]
    return widget.options(widget_context["name"], widget_context["value"], attrs)
