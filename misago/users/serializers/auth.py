from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import ugettext_lazy, ugettext as _

from misago.acl import serialize_acl
from misago.users.authmixin import AuthMixin
from misago.users.tokens import is_password_change_token_valid

from .user import UserSerializer


UserModel = get_user_model()

__all__ = [
    'AuthenticatedUserSerializer',
    'AnonymousUserSerializer',
    'LoginSerializer',
    'ResendActivationSerializer',
    'SendPasswordFormSerializer',
    'ChangePasswordSerializer',
]


class AuthenticatedUserSerializer(UserSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = UserSerializer.Meta.fields + [
            'is_hiding_presence',
            'limits_private_thread_invites_to',
            'unread_private_threads',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads',
        ]

    def get_acl(self, obj):
        return serialize_acl(obj)

    def get_email(self, obj):
        return obj.email

    def get_api(self, obj):
        return {
            'avatar': reverse('misago:api:user-avatar', kwargs={'pk': obj.pk}),
            'details': reverse('misago:api:user-details', kwargs={'pk': obj.pk}),
            'change_email': reverse('misago:api:user-change-email', kwargs={'pk': obj.pk}),
            'change_password': reverse('misago:api:user-change-password', kwargs={'pk': obj.pk}),
            'edit_details': reverse('misago:api:user-edit-details', kwargs={'pk': obj.pk}),
            'options': reverse('misago:api:user-forum-options', kwargs={'pk': obj.pk}),
            'username': reverse('misago:api:user-username', kwargs={'pk': obj.pk}),
        }


AuthenticatedUserSerializer = AuthenticatedUserSerializer.exclude_fields(
    'is_avatar_locked',
    'is_blocked',
    'is_followed',
    'is_signature_locked',
    'meta',
    'signature',
    'status',
)


class AnonymousUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    acl = serializers.SerializerMethodField()

    def get_acl(self, obj):
        if hasattr(obj, 'acl_cache'):
            return serialize_acl(obj)
        else:
            return {}


class LoginSerializer(serializers.Serializer, AuthMixin):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, trim_whitespace=False)

    def validate(self, data):
        user = self.authenticate(data.get('username'), data.get('password'))
        self.confirm_login_allowed(user)
        return {'user': user}


class GetUserSerializer(serializers.Serializer, AuthMixin):
    email = serializers.EmailField(max_length=255)

    def validate(self, data):
        user = self.get_user_by_email(data.get('email'))
        self.confirm_allowed(user)
        return {'user': user}

    def confirm_allowed(self, user):
        """override this method to include additional checks"""
        pass


class ResendActivationSerializer(GetUserSerializer):
    def confirm_allowed(self, user):
        username_format = {'user': user.username}
        if not user.requires_activation:
            message = _("%(user)s, your account is already active.")
            raise ValidationError(message % username_format)
        if user.requires_activation_by_admin:
            message = _("%(user)s, only administrator may activate your account.")
            raise ValidationError(message % username_format)


class SendPasswordFormSerializer(GetUserSerializer):
    auth_messages = {
        'inactive_user': ugettext_lazy(
            "You have to activate your account before "
            "you will be able to request new password."
        ),
        'inactive_admin': ugettext_lazy(
            "Administrator has to activate your account before "
            "you will be able to request new password."
        ),
    }

    def confirm_allowed(self, user):
        self.confirm_user_active(user)


class ChangePasswordSerializer(serializers.Serializer, AuthMixin):
    password = serializers.CharField(
        max_length=255,
        trim_whitespace=False,
    )
    token = serializers.CharField(max_length=255)

    auth_messages = {
        'inactive_user': ugettext_lazy(
            "You have to activate your account before "
            "you will be able to change your password."
        ),
        'inactive_admin': ugettext_lazy(
            "Administrator has to activate your account before "
            "you will be able to change your password."
        ),
    }

    def confirm_allowed(self):
        self.confirm_user_active(self.instance)
        self.confirm_user_not_banned(self.instance)

    def validate_password(self, value):
        validate_password(value, user=self.instance)
        return value

    def validate_token(self, value):
        if not is_password_change_token_valid(self.instance, value):
            raise ValidationError(_("Form link is invalid or expired. Please try again."))
        return value

    def validate(self, data):
        self.confirm_allowed()
        return data

    def save(self):
        self.instance.set_password(self.validated_data['password'])
        self.instance.save()
