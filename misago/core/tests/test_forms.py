from django.test import TestCase
from misago.core import forms


class MockForm(forms.Form):
    stripme = forms.CharField(required=False)
    autostrip_exclude = ['dontstripme']
    dontstripme = forms.CharField(required=False)


class MisagoFormsTests(TestCase):
    def test_stripme_input_is_autostripped(self):
        """Automatic strip worked on stripme input"""
        form = MockForm({'stripme': u' Ni! '})
        form.full_clean()
        self.assertEqual(form.cleaned_data['stripme'], 'Ni!')

    def test_dontstripme_input_is_ignored(self):
        """Automatic strip ignored dontstripme input"""
        form = MockForm({'dontstripme': u' Ni! '})
        form.full_clean()
        self.assertEqual(form.cleaned_data['dontstripme'], ' Ni! ')


class YesNoForm(forms.Form):
    test_field = forms.YesNoSwitch(label='Hello!')


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
