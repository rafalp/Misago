from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from ..users.validators import (
    validate_username_content,
    validate_username_banned,
    validate_email_content,
    validate_email_banned,
)


class UserDataValidator(forms.Form):
    id = forms.IntegerField(min_value=1)
    username = forms.CharField()
    email = forms.CharField()
    is_active = forms.BooleanField(required=False)

    def clean_username(self):
        data = self.cleaned_data["username"]

        validate_username_content(data)
        if validate_username_banned(data):
            raise ValidationError(_("This username is not allowed."))

        return data

    def clean_email(self):
        data = self.cleaned_data["email"]

        validate_email_content(data)
        if validate_email_banned(data):
            raise ValidationError(_("This e-mail address is not allowed."))

        return data
