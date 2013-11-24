from django import forms
from misago.forms import Form

class QuickFindUserForm(Form):
    username = forms.CharField()