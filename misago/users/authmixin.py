from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy, ugettext as _

from misago.core.exceptions import Banned
from misago.users.bans import get_user_ban


UserModel = get_user_model()


class AuthMixin(object):
    """
    Mixin with utils for Auth forms and serializers
    """
    auth_messages = {
        'empty_data': ugettext_lazy("Fill out both fields."),
        'invalid_login': ugettext_lazy("Login or password is incorrect."),
        'inactive_user': ugettext_lazy("You have to activate your account before you will be able to sign in."),
        'inactive_admin': ugettext_lazy(
            "Your account has to be activated by Administrator before you will be able to sign in."
        ),
    }

    def authenticate(self, username, password):
        if username and password:
            user = authenticate(username=username, password=password)

            if user is None or not user.is_active:
                self.raise_for_code('invalid_login')
        else:
            self.raise_for_code('empty_data')

        return user

    def get_user_by_email(self, email):
        if not email:
            return None

        try:
            user = UserModel.objects.get_by_email(email)
            if not user.is_active:
                raise UserModel.DoesNotExist()
            return user
        except UserModel.DoesNotExist:
            raise ValidationError(_("No user with this e-mail exists."))

    def confirm_login_allowed(self, user):
        self.confirm_user_active(user)
        self.confirm_user_not_banned(user)

    def confirm_user_active(self, user):
        if user.requires_activation_by_admin:
            self.raise_for_code('inactive_admin')
        if user.requires_activation_by_user:
            self.raise_for_code('inactive_user')

    def confirm_user_not_banned(self, user):
        ban = self.get_user_ban(user)
        if ban:
            raise Banned(ban=ban)

    def get_user_ban(self, user):
        if user.is_staff:
            return None
        return get_user_ban(user)

    def raise_if_banned(self):
        user = self.validated_data.get('user')
        self.confirm_user_not_banned(user)

    def raise_for_code(self, code):
        raise ValidationError(self.auth_messages[code], code=code)
