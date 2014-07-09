from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase
from misago.core import forms


class CaptureTests(TestCase):
    def setUp(self):
        self.context = Context({'unsafe_name': 'The<hr>Html'})

    def test_capture(self):
        """capture content to variable"""
        tpl_content = """
{% load misago_capture %}

{% capture as the_var %}
{{ unsafe_name }}
{% endcapture %}
Hello, <b>{{ the_var|safe }}</b>
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn('The&lt;hr&gt;Html', render)
        self.assertNotIn('<b>The&lt;hr&gt;Html</b>', render)

    def test_capture_trimmed(self):
        """capture trimmed content to variable"""
        tpl_content = """
{% load misago_capture %}

{% capture trimmed as the_var %}
{{ unsafe_name }}
{% endcapture %}
Hello, <b>{{ the_var|safe }}</b>
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn('<b>The&lt;hr&gt;Html</b>', render)


class TestForm(forms.Form):
    somefield = forms.CharField(label="Hello!", max_length=255)


class FormRowTests(TestCase):
    def setUp(self):
        self.context = Context({'form': TestForm()})

    def test_form_row_no_args(self):
        """form_row with no args renders form row"""
        tpl_content = """
{% load misago_forms %}

{% form_row form.somefield %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn('id_somefield', render)

    def test_form_row_with_args(self):
        """form_row with args renders form row"""
        tpl_content = """
{% load misago_forms %}

{% form_row form.somefield "col-md-3" "col-md-9" %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()

        self.assertIn('id_somefield', render)
        self.assertIn('col-md-3', render)
        self.assertIn('col-md-9', render)

    def test_form_row_with_value_args(self):
        """form_row with values args renders form row"""
        tpl_content = """
{% load misago_forms %}

{% with label="col-md-3" field="col-md-9" %}
    {% form_row form.somefield label field %}
{% endwith %}
"""

        tpl = Template(tpl_content)
        render = tpl.render(self.context).strip()
        self.assertIn('id_somefield', render)
        self.assertIn('col-md-3', render)
        self.assertIn('col-md-9', render)

    def test_form_row_with_no_args(self):
        """form_row with no args raises exception"""
        tpl_content = """
{% load misago_forms %}

{% form_row %}
"""

        with self.assertRaises(TemplateSyntaxError):
            tpl = Template(tpl_content)
            render = tpl.render(self.context).strip()

    def test_form_row_with_two_args(self):
        """form_row with two args raises exception"""
        tpl_content = """
{% load misago_forms %}

{% form_row form.somefield "col-md-9" %}
"""

        with self.assertRaises(TemplateSyntaxError):
            tpl = Template(tpl_content)
            render = tpl.render(self.context).strip()

    def test_form_row_with_four_args(self):
        """form_row with four args raises exception"""
        tpl_content = """
{% load misago_forms %}

{% form_row form.somefield "col-md-9" "col-md-9" "col-md-9" %}
"""

        with self.assertRaises(TemplateSyntaxError):
            tpl = Template(tpl_content)
            render = tpl.render(self.context).strip()
