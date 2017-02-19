from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings
from misago.core.forms import YesNoSwitch
from misago.users.validators import validate_email


UserModel = get_user_model()

__all__ = [
    'ForumOptionsSerializer',
    'EditSignatureSerializer',
    'ChangePasswordSerializer',
    'ChangeEmailSerializer',
]


class ForumOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'is_hiding_presence',
            'limits_private_thread_invites_to',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads'
        ]
        extra_kwargs = {
            'limits_private_thread_invites_to': {
                'required': True
            },
            'subscribe_to_started_threads': {
                'required': True
            },
            'subscribe_to_replied_threads': {
                'required': True
            },
        }


class EditSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['signature']

    def validate(self, data):
        if len(data.get('signature', '')) > settings.signature_length_max:
            raise serializers.ValidationError(_("Signature is too long."))

        return data


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    new_password = serializers.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)

    def validate_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError(_("Entered password is invalid."))
        return value

    def validate_new_password(self, value):
        validate_password(value, user=self.user)
        return value


class ChangeEmailSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    new_email = serializers.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeEmailSerializer, self).__init__(*args, **kwargs)

    def validate_password(self, value):
        if not self.user.check_password(value):
            raise serializers.ValidationError(_("Entered password is invalid."))
        return value

    def validate_new_email(self, value):
        if not value:
            raise serializers.ValidationError(_("You have to enter new e-mail address."))

        if value.lower() == self.user.email.lower():
            raise serializers.ValidationError(_("New e-mail is same as current one."))

        validate_email(value)

        return value
