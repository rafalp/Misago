from django import forms, template
from django.utils.html import format_html_join

from ..forms import YesNoSwitchBase

register = template.Library()


@register.inclusion_tag("misago/admin/form/row.html")
def form_row(field, label_class=None, field_class=None):
    return {"field": field, "label_class": label_class, "field_class": field_class}


@register.inclusion_tag("misago/admin/form/dimensions_row.html")
def form_dimensions_row(field_width, field_height, label_class=None, field_class=None):
    return {
        "field_width": field_width,
        "field_height": field_height,
        "label_class": label_class,
        "field_class": field_class,
    }


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
    attrs = {"id": field.auto_id}
    if field.field.disabled:
        attrs["disabled"] = True
    elif field.field.required:
        attrs["required"] = True

    context = field.field.widget.get_context(field.html_name, field.value(), attrs)
    context["field"] = field
    return context


@register.simple_tag
def render_attrs(attrs, class_name=None):
    rendered_attrs = []
    for attr, value in attrs.items():
        if value not in (True, False, None):
            rendered_attrs.append((attr, value))
    if not attrs.get("class") and class_name:
        rendered_attrs.append(("class", class_name))
    return format_html_join(" ", '{}="{}"', rendered_attrs)


BOOL_ATTRS = ("selected", "checked", "disabled", "required", "readonly")


@register.simple_tag
def render_bool_attrs(attrs):
    attrs_html = []
    for attr, value in attrs.items():
        if attr in BOOL_ATTRS and value is True:
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


MULTIPLE_CHOICE_WIDGETS = (forms.CheckboxSelectMultiple, forms.SelectMultiple)


@register.filter
def is_multiple_choice_field(field):
    return isinstance(field.field.widget, MULTIPLE_CHOICE_WIDGETS)


@register.filter
def is_textarea_field(field):
    return isinstance(field.field.widget, forms.Textarea)


@register.filter
def get_options(widget):
    """Filter that extracts field choices into an easily iterable list"""
    options = []
    for _, optgroup, _ in widget["optgroups"]:
        options += optgroup
    return options
