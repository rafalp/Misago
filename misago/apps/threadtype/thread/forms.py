from django import forms
from misago.forms import Form
from misago.apps.threadtype.mixins import ValidatePostLengthMixin

class QuickReplyForm(Form, ValidatePostLengthMixin):
    post = forms.CharField(widget=forms.Textarea)