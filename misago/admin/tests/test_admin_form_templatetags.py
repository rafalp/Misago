from unittest.mock import Mock

import pytest
from django import forms
from django.template import Context, Template, TemplateSyntaxError

from ..forms import YesNoSwitch
from ..templatetags.misago_admin_form import (
    get_field_image_dimensions,
    is_multiple_choice_field,
    is_radio_select_field,
    is_select_field,
    is_textarea_field,
    is_yesno_switch_field,
    render_attrs,
    render_bool_attrs,
)


class Form(forms.Form):
    text_field = forms.CharField(
        label="Hello!", max_length=255, help_text="I am a help text."
    )
    textarea_field = forms.CharField(
        label="Message", max_length=255, widget=forms.Textarea()
    )
    select_field = forms.ChoiceField(
        label="Choice", choices=(("y", "Yes"), ("n", "No"))
    )
    checkbox_select_field = forms.MultipleChoiceField(
        label="Color",
        choices=(("r", "Red"), ("g", "Green"), ("b", "Blue")),
        widget=forms.CheckboxSelectMultiple,
    )
    multiple_select_field = forms.MultipleChoiceField(
        label="Rank", choices=(("r", "Red"), ("g", "Green"), ("b", "Blue"))
    )
    yesno_field = YesNoSwitch(label="Switch")
    image_field = forms.ImageField(label="Image!", help_text="I am a help text.")


@pytest.fixture
def form():
    return Form()


def render(template_str, form=None):
    base_template = "{%% load misago_admin_form %%} %s"
    context = Context({"form": form or Form()})
    template = Template(base_template % template_str)
    return template.render(context).strip()


def test_row_with_field_input_is_rendered():
    html = render("{% form_row form.text_field %}")
    assert "id_text_field" in html


def test_row_with_field_input_and_label_css_class_is_rendered():
    html = render('{% form_row form.text_field label_class="col-md-3" %}')
    assert "id_text_field" in html
    assert "col-md-3" in html


def test_row_with_field_input_and_field_css_class_is_rendered():
    html = render('{% form_row form.text_field field_class="col-md-9" %}')
    assert "id_text_field" in html
    assert "col-md-9" in html


def test_row_with_field_input_and_label_and_field_css_classes_is_rendered():
    html = render('{% form_row form.text_field "col-md-3" "col-md-9" %}')
    assert "id_text_field" in html
    assert "col-md-3" in html
    assert "col-md-9" in html


def test_field_label_is_rendered():
    html = render("{% form_row form.text_field %}")
    assert "Hello!" in html


def test_field_help_text_is_rendered():
    html = render("{% form_row form.text_field %}")
    assert "I am a help text." in html


def test_tag_without_field_raises_exception():
    with pytest.raises(TemplateSyntaxError):
        render("{% form_row %}")


def test_image_row_with_field_input_is_rendered():
    html = render("{% form_image_row form.image_field %}")
    assert "id_image_field" in html


def test_image_row_with_field_input_and_label_css_class_is_rendered():
    html = render('{% form_image_row form.image_field label_class="col-md-3" %}')
    assert "id_image_field" in html
    assert "col-md-3" in html


def test_image_row_with_field_input_and_field_css_class_is_rendered():
    html = render('{% form_image_row form.image_field field_class="col-md-9" %}')
    assert "id_image_field" in html
    assert "col-md-9" in html


def test_image_row_with_field_input_and_label_and_field_css_classes_is_rendered():
    html = render('{% form_image_row form.image_field "col-md-3" "col-md-9" %}')
    assert "id_image_field" in html
    assert "col-md-3" in html
    assert "col-md-9" in html


def test_image_field_label_is_rendered():
    html = render("{% form_image_row form.image_field %}")
    assert "Image!" in html


def test_image_field_help_text_is_rendered():
    html = render("{% form_image_row form.image_field %}")
    assert "I am a help text." in html


class TestImage:
    url = "test-image.png"


def render_image(template_str):
    base_template = "{%% load misago_admin_form %%} %s"
    context = Context({"form": Form(initial={"image_field": TestImage()})})
    template = Template(base_template % template_str)
    return template.render(context).strip()


def test_image_row_with_value_renders_label():
    html = render_image("{% form_image_row form.image_field %}")
    assert "Image!" in html


def test_image_row_with_value_renders_help_text():
    html = render_image("{% form_image_row form.image_field %}")
    assert "I am a help text." in html


def test_image_row_with_value_renders_image_preview():
    html = render_image("{% form_image_row form.image_field %}")
    assert ('src="%s"' % TestImage.url) in html


def test_image_row_with_value_renders_input():
    html = render_image("{% form_image_row form.image_field %}")
    assert "id_image_field" in html


def test_image_row_with_value_renders_input_and_label_css_class():
    html = render_image('{% form_image_row form.image_field label_class="col-md-3" %}')
    assert "id_image_field" in html
    assert "col-md-3" in html


def test_image_row_with_value_renders_input_and_field_css_class():
    html = render_image('{% form_image_row form.image_field field_class="col-md-9" %}')
    assert "id_image_field" in html
    assert "col-md-9" in html


def test_image_row_with_value_renders_input_and_label_and_field_css_classes():
    html = render_image('{% form_image_row form.image_field "col-md-3" "col-md-9" %}')
    assert "id_image_field" in html
    assert "col-md-3" in html
    assert "col-md-9" in html


def test_image_tag_without_field_raises_exception():
    with pytest.raises(TemplateSyntaxError):
        render("{% form_image_row %}")


def test_for_field_with_radio_select_widget_filter_returns_true(form):
    assert is_radio_select_field(form["yesno_field"])


def test_for_field_without_radio_select_widget_filter_returns_false(form):
    assert not is_radio_select_field(form["text_field"])


def test_for_field_with_select_widget_filter_returns_true(form):
    assert is_select_field(form["select_field"])


def teste_for_field_without_select_widget_filter_returns_false(form):
    assert not is_select_field(form["text_field"])


def test_for_field_with_checkbox_select_widget_filter_returns_true(form):
    assert is_multiple_choice_field(form["checkbox_select_field"])


def test_for_field_without_checkbox_select_widget_filter_returns_false(form):
    assert not is_multiple_choice_field(form["text_field"])


def test_for_field_with_multiple_select_widget_filter_returns_true(form):
    assert is_multiple_choice_field(form["multiple_select_field"])


def test_for_field_without_multiple_select_widget_filter_returns_false(form):
    assert not is_multiple_choice_field(form["text_field"])


def test_for_field_with_textarea_widget_filter_returns_true(form):
    assert is_textarea_field(form["textarea_field"])


def test_for_field_without_textarea_widget_filter_returns_false(form):
    assert not is_textarea_field(form["text_field"])


def test_for_yes_no_field_filter_returns_true(form):
    assert is_yesno_switch_field(form["yesno_field"])


def test_for_non_yes_no_field_filter_returns_false(form):
    assert not is_yesno_switch_field(form["text_field"])


def test_specified_class_name_is_rendered():
    result = render_attrs({"attrs": {}}, class_name="form-control")
    assert result == 'class="form-control"'


def test_specified_class_name_overrided_by_class_attr():
    result = render_attrs({"attrs": {"class": "custom"}}, class_name="form-control")
    assert result == 'class="custom"'


def test_attr_with_string_value_is_rendered():
    result = render_attrs({"attrs": {"name": "lorem"}})
    assert result == 'name="lorem"'


def test_attr_with_int_value_is_rendered():
    result = render_attrs({"attrs": {"cols": 5}})
    assert result == 'cols="5"'


def test_attr_with_boolean_true_value_is_not_rendered():
    result = render_attrs({"attrs": {"selected": True}})
    assert result == ""


def test_attr_with_boolean_false_value_is_not_rendered():
    result = render_attrs({"attrs": {"selected": False}})
    assert result == ""


def test_attr_with_none_value_is_not_rendered():
    result = render_attrs({"attrs": {"selected": None}})
    assert result == ""


def test_attr_name_is_escaped():
    result = render_attrs({"attrs": {'"': "test"}})
    assert result == '&quot;="test"'


def test_attr_value_is_escaped():
    result = render_attrs({"attrs": {"name": '"'}})
    assert result == 'name="&quot;"'


def test_multiple_valid_attrs_are_rendered():
    result = render_attrs({"attrs": {"name": "lorem", "cols": 5}})
    assert result == 'name="lorem" cols="5"'


def test_empty_attr_dict_is_not_rendered():
    result = render_attrs({"attrs": {}})
    assert result == ""


def test_attr_with_boolean_true_value_is_rendered():
    result = render_bool_attrs({"bool": True})
    assert result == "bool"


def test_bool_attr_with_string_value_is_not_rendered():
    result = render_bool_attrs({"name": "hello"})
    assert result == ""


def test_bool_attr_with_int_value_is_not_rendered():
    result = render_bool_attrs({"col": 13})
    assert result == ""


def test_bool_attr_with_boolean_false_value_is_not_rendered():
    result = render_bool_attrs({"selected": False})
    assert result == ""


def test_bool_attr_with_none_value_is_not_rendered():
    result = render_bool_attrs({"selected": None})
    assert result == ""


def test_bool_attr_with_false_int_value_is_not_rendered():
    result = render_bool_attrs({"selected": 0})
    assert result == ""


def test_multiple_bool_attrs_with_boolean_true_value_are_rendered():
    result = render_bool_attrs({"selected": True, "required": True})
    assert result == "selected required"


def test_only_bool_attrs_with_boolean_true_value_are_rendered():
    result = render_bool_attrs({"bool": True, "string": "hello", "int": 123})
    assert result == "bool"


def test_util_turns_dimensions_tuple_into_dict():
    assert get_field_image_dimensions((20, 40)) == {"width": 20, "height": 40}


def test_util_returs_none_if_dimensions_are_empty():
    assert get_field_image_dimensions(None) is None
