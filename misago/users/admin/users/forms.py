from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.acl.models import Role
from misago.forms import Form
from misago.users.models import Rank

class SearchUsersForm(Form):
    username = forms.CharField(max_length=255, required=False)
    email = forms.CharField(max_length=255, required=False)
    activation = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=(('0', _("Already Active")), ('1', _("By User")), ('2', _("By Administrator")), ('3', _("Sign-In Credentials Change"))), required=False)
    rank = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Rank.objects.order_by('order').all(), required=False)
    role = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Role.objects.order_by('name').all(), required=False)
    
    layout = (
              (
               _("Search Users"),
               (
                ('username', {'label': _("Username"), 'attrs': {'placeholder': _("Username contains...")}}),
                ('email', {'label': _("E-mail Address"), 'attrs': {'placeholder': _("E-mail address contains...")}}),
                ('activation', {'label': _("Activation Requirement")}),
                ('rank', {'label': _("Rank is")}),
                ('role', {'label': _("Has Role")}),
               ),
              ),
             )
    