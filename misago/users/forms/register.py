from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from ..bans import get_email_ban, get_ip_ban, get_username_ban
from ..validators import validate_email, validate_new_registration, validate_username

User = get_user_model()


class BaseRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField(validators=[validate_email])

    terms_of_service = forms.IntegerField(required=False)
    privacy_policy = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.agreements = kwargs.pop("agreements")
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_username(self):
        data = self.cleaned_data["username"]

        validate_username(self.request.settings, data)
        ban = get_username_ban(data, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("This usernane is not allowed."))
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]

        ban = get_email_ban(data, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("This e-mail address is not allowed."))
        return data

    def clean_agreements(self, data):
        for field_name, agreement in self.agreements.items():
            if data.get(field_name) != agreement["id"]:
                error = ValueError(_("This agreement is required."))
                self.add_error(field_name, error)

    def raise_if_ip_banned(self):
        ban = get_ip_ban(self.request.user_ip, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(
                    _("New registrations from this IP address are not allowed.")
                )


class SocialAuthRegisterForm(BaseRegisterForm):
    def clean(self):
        cleaned_data = super().clean()

        self.clean_agreements(cleaned_data)
        self.raise_if_ip_banned()

        validate_new_registration(self.request, cleaned_data, self.add_error)

        return cleaned_data


class RegisterForm(BaseRegisterForm):
    password = forms.CharField(strip=False)

    # placeholder field for setting captcha errors on form
    captcha = forms.CharField(required=False)

    def full_clean_password(self, cleaned_data):
        if cleaned_data.get("password"):
            validate_password(
                cleaned_data["password"],
                user=User(
                    username=cleaned_data.get("username"),
                    email=cleaned_data.get("email"),
                ),
            )

    def clean(self):
        cleaned_data = super().clean()

        self.clean_agreements(cleaned_data)
        self.raise_if_ip_banned()

        try:
            self.full_clean_password(cleaned_data)
        except forms.ValidationError as e:
            self.add_error("password", e)

        validate_new_registration(self.request, cleaned_data, self.add_error)

        return cleaned_data
