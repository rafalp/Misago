from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (AuthenticationForm as
                                       BaseAuthenticationForm)
from django.template.defaultfilters import date as format_date
from django.utils.translation import ugettext_lazy as _

from misago.core import forms
from misago.users.bans import get_user_ban


class AuthenticationForm(forms.Form, BaseAuthenticationForm):
    """
    Base class for authenticating users, Floppy-forms and
    Misago login field comliant
    """
    username = forms.CharField(label=_("Username or e-mail"),
                               required=False,
                               max_length=254)
    password = forms.CharField(label=_("Password"), required=False,
                               widget=forms.PasswordInput)

    error_messages = {
        'empty_data': _("You have to fill out both fields."),
        'invalid_login': _("Your login or password is incorrect."),
        'inactive_user': _("You have to activate your account before "
                           "you will be able to sign in."),
        'inactive_admin': _("Administrator has to activate your account "
                            "before you will be able to sign in."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None or not self.user_cache.is_active:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        else:
            raise ValidationError(
                self.error_messages['empty_data'],
                code='empty_data',
            )

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if user.requires_activation_by_admin:
            raise ValidationError(
                self.error_messages['inactive_admin'],
                code='inactive_admin',
            )

        if user.requires_activation_by_user:
            raise ValidationError(
                self.error_messages['inactive_user'],
                code='inactive_user',
            )

        self.user_ban = get_user_ban(user)
        if self.user_ban:
            if self.user_ban.valid_until:
                if self.user_ban.user_message:
                    message = _("%(username)s, your account is "
                                "banned until %(date)s for:")
                else:
                    message = _("%(username)s, your account "
                                "is banned until %(date)s.")
                date_format = {'date': format_date(self.user_ban.valid_until)}
                message = message % date_format
            else:
                if self.user_ban.user_message:
                    message = _("%(username)s, your account is banned for:")
                else:
                    message = _("%(username)s, your account is banned.")

            raise ValidationError(
                message % {'username': self.user_cache.username},
                code='banned',
            )


class AdminAuthenticationForm(AuthenticationForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.error_messages.update({
            'not_staff': _("Your account does not have admin privileges.")
            })

        super(AdminAuthenticationForm, self).__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise forms.ValidationError(
                self.error_messages['not_staff'],
                code='not_staff',
            )
