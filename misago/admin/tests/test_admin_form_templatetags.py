from django import forms
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase

from misago.admin.templatetags.misago_admin_form import (
    is_radio_select_field, is_select_field, is_multiple_choice_field, is_textarea_field,
    render_attrs, render_bool_attrs
)
from misago.admin.forms import YesNoSwitch


class TestForm(forms.Form):
    text_field = forms.CharField(label="Hello!", max_length=255, help_text="I am a help text.")
    textarea_field = forms.CharField(label="Message", max_length=255, widget=forms.Textarea())
    select_field = forms.ChoiceField(label="Choice", choices=(("y", "Yes"), ("n", "No")))
    checkbox_select_field = forms.MultipleChoiceField(
        label="Color",
        choices=(("r", "Red"), ("g", "Green"), ("b", "Blue")),
        widget=forms.CheckboxSelectMultiple,
    )
    multiple_select_field = forms.MultipleChoiceField(
        label="Rank",
        choices=(("r", "Red"), ("g", "Green"), ("b", "Blue")),
    )
    yesno_field = YesNoSwitch(label="Switch")


def render(template_str):
    base_template = "{%% load misago_admin_form %%} %s"
    context = Context({'form': TestForm()})
    template = Template(base_template % template_str)
    return template.render(context).strip()


class FormRowTagTests(TestCase):
    def test_row_with_field_input_is_rendered(self):
        html = render("{% form_row form.text_field %}")
        self.assertIn('id_text_field', html)

    def test_row_with_field_input_and_label_css_class_is_rendered(self):
        html = render('{% form_row form.text_field label_class="col-md-3" %}')
        self.assertIn('id_text_field', html)
        self.assertIn('col-md-3', html)

    def test_row_with_field_input_and_field_css_class_is_rendered(self):
        html = render('{% form_row form.text_field field_class="col-md-9" %}')
        self.assertIn('id_text_field', html)
        self.assertIn('col-md-9', html)

    def test_row_with_field_input_and_label_andfield_css_classes_is_rendered(self):
        html = render('{% form_row form.text_field "col-md-3" "col-md-9" %}')
        self.assertIn('id_text_field', html)
        self.assertIn('col-md-3', html)
        self.assertIn('col-md-9', html)

    def test_tag_without_field_raises_exception(self):
        with self.assertRaises(TemplateSyntaxError):
            render('{% form_row %}')

    def test_field_label_is_rendered(self):
        html = render("{% form_row form.text_field %}")
        self.assertIn("Hello!", html)

    def test_field_help_text_is_rendered(self):
        html = render("{% form_row form.text_field %}")
        self.assertIn("I am a help text.", html)


class IsRadioSelectFieldFilterTests(TestCase):
    def test_for_field_with_radio_select_widget_filter_returns_true(self):
        form = TestForm()
        self.assertTrue(is_radio_select_field(form['yesno_field']))

    def test_for_field_without_radio_select_widget_filter_returns_false(self):
        form = TestForm()
        self.assertFalse(is_radio_select_field(form['text_field']))


class IsSelectFieldFilerTests(TestCase):
    def test_for_field_with_select_widget_filter_returns_true(self):
        form = TestForm()
        self.assertTrue(is_select_field(form['select_field']))

    def teste_for_field_without_select_widget_filter_returns_false(self):
        form = TestForm()
        self.assertFalse(is_select_field(form['text_field']))


class IsMultipleChoiceFieldFilerTests(TestCase):
    def test_for_field_with_checkbox_select_widget_filter_returns_true(self):
        form = TestForm()
        self.assertTrue(is_multiple_choice_field(form['checkbox_select_field']))

    def test_for_field_without_checkbox_select_widget_filter_returns_false(self):
        form = TestForm()
        self.assertFalse(is_multiple_choice_field(form['text_field']))

    def test_for_field_with_multiple_select_widget_filter_returns_true(self):
        form = TestForm()
        self.assertTrue(is_multiple_choice_field(form['multiple_select_field']))

    def test_for_field_without_multiple_select_widget_filter_returns_false(self):
        form = TestForm()
        self.assertFalse(is_multiple_choice_field(form['text_field']))


class IsTextareaFieldFilterTests(TestCase):
    def test_for_field_with_textarea_widget_filter_returns_true(self):
        form = TestForm()
        self.assertTrue(is_textarea_field(form['textarea_field']))

    def test_for_field_without_textarea_widget_filter_returns_false(self):
        form = TestForm()
        self.assertFalse(is_textarea_field(form['text_field']))


class RenderAttrsTagTests(TestCase):
    def test_specified_class_name_is_rendered(self):
        result = render_attrs({"attrs": {}}, class_name="form-control")
        self.assertEqual(result, 'class="form-control"')

    def test_specified_class_name_overrided_by_class_attr(self):
        result = render_attrs({"attrs": {"class": "custom"}}, class_name="form-control")
        self.assertEqual(result, 'class="custom"')

    def test_attr_with_string_value_is_rendered(self):
        result = render_attrs({"attrs": {"name": "lorem"}})
        self.assertEqual(result, 'name="lorem"')

    def test_attr_with_int_value_is_rendered(self):
        result = render_attrs({"attrs": {"cols": 5}})
        self.assertEqual(result, 'cols="5"')

    def test_attr_with_boolean_true_value_is_not_rendered(self):
        result = render_attrs({"attrs": {"selected": True}})
        self.assertEqual(result, "")

    def test_attr_with_boolean_false_value_is_not_rendered(self):
        result = render_attrs({"attrs": {"selected": False}})
        self.assertEqual(result, "")

    def test_attr_with_none_value_is_not_rendered(self):
        result = render_attrs({"attrs": {"selected": None}})
        self.assertEqual(result, "")

    def test_attr_name_is_escaped(self):
        result = render_attrs({"attrs": {'"': 'test'}})
        self.assertEqual(result, '&quot;="test"')

    def test_attr_value_is_escaped(self):
        result = render_attrs({"attrs": {"name": '"'}})
        self.assertEqual(result, 'name="&quot;"')

    def test_multiple_valid_attrs_are_rendered(self):
        result = render_attrs({"attrs": {"name": "lorem", "cols": 5}})
        self.assertEqual(result, 'name="lorem" cols="5"')

    def test_empty_attr_dict_is_not_rendered(self):
        result = render_attrs({"attrs": {}})
        self.assertEqual(result, "")


class RenderBoolAttrsTagTests(TestCase):
    def test_attr_with_boolean_true_value_is_rendered(self):
        result = render_bool_attrs({"bool": True})
        self.assertEqual(result, "bool")

    def test_attr_with_string_value_is_not_rendered(self):
        result = render_bool_attrs({"name": "hello"})
        self.assertEqual(result, "")

    def test_attr_with_int_value_is_not_rendered(self):
        result = render_bool_attrs({"col": 13})
        self.assertEqual(result, "")

    def test_attr_with_boolean_false_value_is_not_rendered(self):
        result = render_bool_attrs({"selected": False})
        self.assertEqual(result, "")

    def test_attr_with_none_value_is_not_rendered(self):
        result = render_bool_attrs({"selected": None})
        self.assertEqual(result, "")

    def test_attr_with_false_int_value_is_not_rendered(self):
        result = render_bool_attrs({"selected": 0})
        self.assertEqual(result, "")

    def test_multiple_attrs_with_boolean_true_value_are_rendered(self):
        result = render_bool_attrs({"selected": True, "required": True})
        self.assertEqual(result, "selected required")

    def test_only_attrs_with_boolean_true_value_are_rendered(self):
        result = render_bool_attrs({"bool": True, "string": "hello", "int": 123})
        self.assertEqual(result, "bool")

    def test_empty_attr_dict_is_not_rendered(self):
        result = render_bool_attrs({})
        self.assertEqual(result, "")