from django.test import TestCase
from misago.core import forms


class MockForm(forms.Form):
    stripme = forms.CharField(required=False)
    autostrip_exclude = ['dontstripme']
    dontstripme = forms.CharField(required=False)


class MisagoFormsTests(TestCase):
    serialized_rollback = True

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
    serialized_rollback = True

    def test_valid_inputs(self):
        """YesNoSwitch returns valid values for valid input"""
        form = YesNoForm({'test_field': u'1'})
        form.full_clean()
        self.assertTrue(form.cleaned_data['test_field'])

        form = YesNoForm({'test_field': u'0'})
        form.full_clean()
        self.assertTrue(not form.cleaned_data['test_field'])

    def test_dontstripme_input_is_ignored(self):
        """YesNoSwitch returns valid values for invalid input"""
        form = YesNoForm({'test_field': u'221'})
        form.full_clean()
        self.assertTrue(form.cleaned_data.get('test_field') is None)
