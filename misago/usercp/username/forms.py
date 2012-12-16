from django import forms
from django.core.exceptions import ValidationError
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
        
        self.request.user.set_username(self.cleaned_data['username'])
        if org_username == self.request.user.username:
            raise ValidationError(_("Your new username is same as current one."))
        
        try:
            self.request.user.full_clean()
        except ValidationError as e:
            self.request.user.is_username_valid(e)
        return self.cleaned_data['username']