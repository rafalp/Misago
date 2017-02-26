from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils.translation import ungettext

from misago.conf import settings


UserModel = get_user_model()

__all__ = [
    'ModerateAvatarSerializer',
    'ModerateSignatureSerializer',
]


class ModerateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'is_avatar_locked',
            'avatar_lock_user_message',
            'avatar_lock_staff_message',
        ]


class ModerateSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'signature',
            'is_signature_locked',
            'signature_lock_user_message',
            'signature_lock_staff_message',
        ]

    def validate_signature(self, value):
        length_limit = settings.signature_length_max
        if len(value) > length_limit:
            raise serializers.ValidationError(
                ungettext(
                    "Signature can't be longer than %(limit)s character.",
                    "Signature can't be longer than %(limit)s characters.",
                    length_limit,
                ) % {'limit': length_limit}
            )

        return value
