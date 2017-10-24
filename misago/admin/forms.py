from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from misago.users.authmixin import AuthMixin


class AdminAuthenticationForm(BaseAuthenticationForm, AuthMixin):
    username = forms.CharField(
        label=_("Username or e-mail"),
        required=False,
        max_length=254,
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        required=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'empty_data': _("Fill out both fields."),
        'invalid_login': _("Login or password is incorrect."),
        'not_staff': _("Your account does not have admin privileges."),
    }
    required_css_class = 'required'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None or not self.user_cache.is_active:
                raise ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            else:
                self.confirm_login_allowed(self.user_cache)
        else:
            raise ValidationError(self.error_messages['empty_data'], code='empty_data')

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise ValidationError(self.error_messages['not_staff'], code='not_staff')
