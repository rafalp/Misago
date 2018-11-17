from django import forms
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase


class TestForm(forms.Form):
    text_field = forms.CharField(label="Hello!", max_length=255)


def render(template_str):
    base_template = "{%% load misago_admin_form %%} %s"
    context = Context({'form': TestForm()})
    template = Template(base_template % template_str)
    return template.render(context).strip()


class FormRowTests(TestCase):
    def test_tag_renders_row_with_field(self):
        html = render("{% form_row form.text_field %}")
        self.assertIn('id_text_field', html)

    def test_tag_with_label_class_option_renders_row_including_css_class(self):
        html = render('{% form_row form.text_field label_class="col-md-3" %}')
        self.assertIn('id_text_field', html)
        self.assertIn('col-md-3', html)

    def test_tag_with_field_class_option_renders_row_including_css_class(self):
        html = render('{% form_row form.text_field field_class="col-md-9" %}')
        self.assertIn('id_text_field', html)
        self.assertIn('col-md-9', html)

    def test_tag_with_label_and_control_options_renders_row_including_both_css_classes(self):
        html = render('{% form_row form.text_field "col-md-3" "col-md-9" %}')
        self.assertIn('id_text_field', html)
        self.assertIn('col-md-3', html)
        self.assertIn('col-md-9', html)

    def test_tag_without_field_raises_exception(self):
        with self.assertRaises(TemplateSyntaxError):
            render('{% form_row %}')
