from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form

class SearchUsersForm(Form):
    """
    Search Users
    """
    username = forms.CharField(max_length=255, required=False)
    email = forms.CharField(max_length=255, required=False)
    activation = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=(('0', _("Already Active")), ('1', _("By User")), ('2', _("By Administrator"))),required=False)
    layout = (
              (
               _("Search Users"),
               (
                ('username', {'label': _("Username"), 'attrs': {'placeholder': _("Username contains...")}}),
                ('email', {'label': _("E-mail Address"), 'attrs': {'placeholder': _("E-mail address contains...")}}),
                ('activation', {'label': _("Activation Requirement")}),
               ),
              ),
             )
    