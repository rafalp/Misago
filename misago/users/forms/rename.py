from django.utils.translation import ugettext_lazy as _

from misago.core import forms
from misago.users.validators import validate_username


class ChangeUsernameForm(forms.Form):
    username = forms.CharField(max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(ChangeUsernameForm, self).clean()
        username = data.get('username')

        if not username:
            raise forms.ValidationError(_("Enter new username."))

        if username == self.user.username:
            message = _("New username is same as current one.")
            raise forms.ValidationError(message)

        validate_username(username, exclude=self.user)

        return data

    def change_username(self, changed_by):
        self.user.set_username(
            self.cleaned_data['username'], changed_by=changed_by)
        self.user.save(update_fields=['username', 'slug'])
