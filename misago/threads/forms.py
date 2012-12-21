from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class NewThreadForm(Form):
    thread_name = forms.CharField(max_length=255)
    post = forms.CharField(widget=forms.Textarea)
    
    layout = [
              [
               None,
               [
                ('thread_name', {'label': _("Thread Name")}),
                ('post', {'label': _("Post Content")}),
                ],
               ],
              ]