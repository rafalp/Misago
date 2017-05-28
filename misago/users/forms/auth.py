from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from misago.users.bans import get_user_ban


UserModel = get_user_model()


class MisagoAuthMixin(object):
    error_messages = {
        'empty_data': _("Fill out both fields."),
        'invalid_login': _("Login or password is incorrect."),
        'inactive_user': _("You have to activate your account before you will be able to sign in."),
        'inactive_admin': _(
            "Your account has to be activated by Administrator before you will be able to sign in."
        ),
    }

    def confirm_user_active(self, user):
        if user.requires_activation_by_admin:
            raise ValidationError(self.error_messages['inactive_admin'], code='inactive_admin')

        if user.requires_activation_by_user:
            raise ValidationError(self.error_messages['inactive_user'], code='inactive_user')

    def confirm_user_not_banned(self, user):
        if not user.is_staff:
            self.user_ban = get_user_ban(user)
            if self.user_ban:
                raise ValidationError('', code='banned')

    def get_errors_dict(self):
        error = self.errors.as_data()['__all__'][0]
        if error.code == 'banned':
            error.message = self.user_ban.ban.get_serialized_message()
        else:
            error.message = error.messages[0]

        return {'detail': error.message, 'code': error.code}


class AuthenticationForm(MisagoAuthMixin, BaseAuthenticationForm):
    """
    Base class for authenticating users, Floppy-forms and
    Misago login field compliant
    """
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
        self.confirm_user_active(user)
        self.confirm_user_not_banned(user)


class AdminAuthenticationForm(AuthenticationForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.error_messages.update({
            'not_staff': _("Your account does not have admin privileges."),
        })

        super(AdminAuthenticationForm, self).__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise forms.ValidationError(self.error_messages['not_staff'], code='not_staff')


class GetUserForm(MisagoAuthMixin, forms.Form):
    email = forms.CharField()

    def clean(self):
        data = super(GetUserForm, self).clean()

        email = data.get('email')
        if not email or len(email) > 250:
            raise forms.ValidationError(_("Enter e-mail address."), code='empty_email')

        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError(_("Entered e-mail is invalid."), code='invalid_email')

        try:
            user = UserModel.objects.get_by_email(data['email'])
            if not user.is_active:
                raise UserModel.DoesNotExist()
            self.user_cache = user
        except UserModel.DoesNotExist:
            raise forms.ValidationError(_("No user with this e-mail exists."), code='not_found')

        self.confirm_allowed(user)

        return data

    def confirm_allowed(self, user):
        """override this method to include additional checks"""


class ResendActivationForm(GetUserForm):
    def confirm_allowed(self, user):
        username_format = {'user': user.username}

        if not user.requires_activation:
            message = _("%(user)s, your account is already active.")
            raise forms.ValidationError(message % username_format, code='already_active')

        if user.requires_activation_by_admin:
            message = _("%(user)s, only administrator may activate your account.")
            raise forms.ValidationError(message % username_format, code='inactive_admin')


class ResetPasswordForm(GetUserForm):
    error_messages = {
        'inactive_user': _(
            "You have to activate your account before "
            "you will be able to request new password."
        ),
        'inactive_admin': _(
            "Administrator has to activate your account before "
            "you will be able to request new password."
        ),
    }

    def confirm_allowed(self, user):
        self.confirm_user_active(user)
