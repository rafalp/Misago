import floppyforms as forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class SignatureForm(Form):
    signature = forms.CharField(widget=forms.Textarea, required=False)
