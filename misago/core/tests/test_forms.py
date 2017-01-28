from django import forms
from django.test import TestCase

from misago.core.forms import YesNoSwitch


class YesNoForm(forms.Form):
    test_field = YesNoSwitch(label='Hello!')


class YesNoSwitchTests(TestCase):
    def test_valid_inputs(self):
        """YesNoSwitch returns valid values for valid input"""
        for true in ('1', 'True', 'true', 1, True):
            form = YesNoForm({'test_field': true})
            form.full_clean()
            self.assertEqual(form.cleaned_data['test_field'], 1)

        for false in ('0', 'False', 'false', 'egebege', False, 0):
            form = YesNoForm({'test_field': false})
            form.full_clean()
            self.assertEqual(form.cleaned_data['test_field'], 0)

    def test_dontstripme_input_is_ignored(self):
        """YesNoSwitch returns valid values for invalid input"""
        form = YesNoForm({'test_field': u'221'})
        form.full_clean()
        self.assertFalse(form.cleaned_data.get('test_field'))
