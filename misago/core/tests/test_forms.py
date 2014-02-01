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
