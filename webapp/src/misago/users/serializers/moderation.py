from django.contrib.auth import get_user_model
from django.utils.translation import ngettext
from rest_framework import serializers

from ...conf import settings

User = get_user_model()

__all__ = ["ModerateAvatarSerializer", "ModerateSignatureSerializer"]


class ModerateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "is_avatar_locked",
            "avatar_lock_user_message",
            "avatar_lock_staff_message",
        ]


class ModerateSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "signature",
            "is_signature_locked",
            "signature_lock_user_message",
            "signature_lock_staff_message",
        ]

    def validate_signature(self, value):
        length_limit = settings.signature_length_max
        if len(value) > length_limit:
            message = ngettext(
                "Signature can't be longer than %(limit)s character.",
                "Signature can't be longer than %(limit)s characters.",
                length_limit,
            )
            raise serializers.ValidationError(message % {"limit": length_limit})

        return value
