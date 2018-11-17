from django import forms
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase


class TestForm(forms.Form):
    somefield = forms.CharField(label="Hello!", max_length=255)


class FormRowTests(TestCase):
    def setUp(self):
        self.context = Context({'form': TestForm()})

    def test_tag_renders_row_with_field(self):
        tpl_content = """
{% load misago_admin_form %}

{% form_row form.somefield %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn('id_somefield', render)

    def test_tag_with_label_class_option_renders_row_including_css_class(self):
        tpl_content = """
{% load misago_admin_form %}

{% form_row form.somefield label_class="col-md-3" %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn('id_somefield', render)
        self.assertIn('col-md-3', render)

    def test_tag_with_field_class_option_renders_row_including_css_class(self):
        tpl_content = """
{% load misago_admin_form %}

{% form_row form.somefield field_class="col-md-9" %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn('id_somefield', render)
        self.assertIn('col-md-9', render)

    def test_tag_with_label_and_control_options_renders_row_including_both_css_classes(self):
        tpl_content = """
{% load misago_admin_form %}

{% form_row form.somefield "col-md-3" "col-md-9" %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()

        self.assertIn('id_somefield', render)
        self.assertIn('col-md-3', render)
        self.assertIn('col-md-9', render)

    def test_tag_without_field_raises_exception(self):
        tpl_content = """
{% load misago_admin_form %}

{% form_row %}
"""

        with self.assertRaises(TemplateSyntaxError):
            Template(tpl_content)
