from django import forms
from misago.forms import Form
from misago.apps.threadtype.mixins import (FloodProtectionMixin,
                                           ValidatePostLengthMixin)

class QuickReplyForm(FloodProtectionMixin, Form, ValidatePostLengthMixin):
    post = forms.CharField(widget=forms.Textarea)