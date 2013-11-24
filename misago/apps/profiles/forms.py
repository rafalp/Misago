import floppyforms as forms
from misago.forms import Form

class QuickFindUserForm(Form):
    username = forms.CharField()