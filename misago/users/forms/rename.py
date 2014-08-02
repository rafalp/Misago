from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.users.validators import validate_username


class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(label=_("New username"), max_length=200,
                                   required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(ChangeUsernameForm, self).clean()
        new_username = data.get('new_username')

        if not new_username:
            raise forms.ValidationError(_("Enter new username."))

        if new_username == self.user.username:
            message = _("New username is same as current one.")
            raise forms.ValidationError(message)

        validate_username(new_username, exclude=self.user)

        return data

    def change_username(self, changed_by):
        self.user.set_username(self.cleaned_data['new_username'],
                          changed_by=changed_by)
        self.user.save(update_fields=['username', 'slug'])
