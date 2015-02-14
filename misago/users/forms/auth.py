from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (AuthenticationForm as
                                       BaseAuthenticationForm)
from django.utils.translation import ugettext_lazy as _

from misago.core import forms
from misago.users.bans import get_user_ban
from misago.users.validators import validate_password


class MisagoAuthMixin(object):
    error_messages = {
        'empty_data': _("Fill out both fields."),
        'invalid_login': _("Login or password is incorrect."),
        'inactive_user': _("You have to activate your account before "
                           "you will be able to sign in."),
        'inactive_admin': _("Your account has to be activated by "
                            "Administrator before you will be able "
                            "to sign in."),
    }

    def confirm_user_active(self, user):
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

    def confirm_user_not_banned(self, user):
        self.user_ban = get_user_ban(user)
        if self.user_ban:
            if self.user_ban.expires_on:
                if self.user_ban.user_message:
                    message = _("%(user)s, your account is "
                                "banned until %(date)s for:")
                else:
                    message = _("%(user)s, your account "
                                "is banned until %(date)s.")
                date_format = {'date': self.user_ban.formatted_expiration_date}
                message = message % date_format
            else:
                if self.user_ban.user_message:
                    message = _("%(user)s, your account is banned for:")
                else:
                    message = _("%(user)s, your account is banned.")

            raise ValidationError(
                message % {'user': self.user_cache.username},
                code='banned',
            )


class AuthenticationForm(MisagoAuthMixin, forms.Form, BaseAuthenticationForm):
    """
    Base class for authenticating users, Floppy-forms and
    Misago login field comliant
    """
    username = forms.CharField(label=_("Username or e-mail"),
                               required=False,
                               max_length=254)
    password = forms.CharField(label=_("Password"), required=False,
                               widget=forms.PasswordInput)

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
        self.confirm_user_active(user)
        self.confirm_user_not_banned(user)


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


class GetUserForm(MisagoAuthMixin, forms.Form):
    username = forms.CharField(label=_("Username or e-mail"))

    def clean(self):
        data = super(GetUserForm, self).clean()

        credential = data.get('username')
        if not credential or len(credential) > 250:
            raise forms.ValidationError(_("You have to fill out form."))

        try:
            User = get_user_model()
            user = User.objects.get_by_username_or_email(data['username'])
            self.user_cache = user
        except User.DoesNotExist:
            raise forms.ValidationError(_("Invalid username or e-mail."))

        self.confirm_allowed(user)

        return data

    def confirm_allowed(self, user):
        raise NotImplementedError("confirm_allowed method must be defined "
                                  "by inheriting classes")


class ResendActivationForm(GetUserForm):
    def confirm_allowed(self, user):
        self.confirm_user_not_banned(user)

        username_format = {'user': user.username}

        if not user.requires_activation:
            message = _("%(user)s, your account is already active.")
            raise forms.ValidationError(message % username_format)

        if user.requires_activation_by_admin:
            message = _("%(user)s, only administrator may activate "
                        "your account.")
            raise forms.ValidationError(message % username_format)


class ResetPasswordForm(GetUserForm):
    error_messages = {
        'inactive_user': _("You have to activate your account before "
                           "you will be able to request new password."),
        'inactive_admin': _("Administrator has to activate your account "
                            "before you will be able to request "
                            "new password."),
    }

    def confirm_allowed(self, user):
        self.confirm_user_not_banned(user)
        self.confirm_user_active(user)


class SetNewPasswordForm(MisagoAuthMixin, forms.Form):
    new_password = forms.CharField(label=_("New password"),
                                   widget=forms.PasswordInput)

    def clean(self):
        data = super(SetNewPasswordForm, self).clean()

        new_password = data.get('new_password')
        if not new_password or len(new_password) > 250:
            raise forms.ValidationError(_("You have to fill out form."))

        validate_password(new_password)

        return data
