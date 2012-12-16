from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form


class SignatureForm(Form):
    signature = forms.CharField(widget=forms.Textarea,required=False)
    
    layout = (
              (
               None,
               (
                ('signature', {'label': _("Your Signature"), 'attrs': {'rows': 10}}),
                )
               ),
              )