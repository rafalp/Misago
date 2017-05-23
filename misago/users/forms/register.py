from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from misago.users import validators
from misago.users.bans import get_email_ban, get_ip_ban, get_username_ban


UserModel = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(validators=[validators.validate_username])
    email = forms.CharField(validators=[validators.validate_email])
    password = forms.CharField(strip=False)

    # placeholder field for setting captcha errors on form
    captcha = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        data = self.cleaned_data['username']

        ban = get_username_ban(data, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("This usernane is not allowed."))
        return data

    def clean_email(self):
        data = self.cleaned_data['email']

        ban = get_email_ban(data, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("This e-mail address is not allowed."))
        return data

    def full_clean_password(self, cleaned_data):
        if cleaned_data.get('password'):
            validate_password(
                cleaned_data['password'],
                user=UserModel(
                    username=cleaned_data.get('username'),
                    email=cleaned_data.get('email'),
                ),
            )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        ban = get_ip_ban(self.request.user_ip, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("New registrations from this IP address are not allowed."))

        try:
            self.full_clean_password(cleaned_data)
        except forms.ValidationError as e:
            self.add_error('password', e)

        validators.validate_new_registration(self.request, self, cleaned_data)

        return cleaned_data
