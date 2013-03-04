from django import forms
from django.core.exceptions import ValidationError
from misago.users.validators import validate_username
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class UsernameChangeForm(Form):
    username = forms.CharField(max_length=255)
    error_source = 'username'

    layout = [
              [
               None,
               [
                ('username', {'label': _("Change Username to"), 'help_text': _("Enter new desired username.")}),
                ],
               ],
              ]

    def clean_username(self):
        org_username = self.request.user.username
        if org_username == self.cleaned_data['username']:
            raise ValidationError(_("Your new username is same as current one."))
        validate_username(self.cleaned_data['username'])
        self.request.user.set_username(self.cleaned_data['username'])
        try:
            self.request.user.full_clean()
        except ValidationError as e:
            self.request.user.is_username_valid(e)
            self.request.user.set_username(org_username)
        return self.cleaned_data['username']
