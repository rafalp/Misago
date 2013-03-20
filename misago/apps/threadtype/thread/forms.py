from django import forms
from misago.forms import Form

class QuickReplyForm(Form):
    post = forms.CharField(widget=forms.Textarea)