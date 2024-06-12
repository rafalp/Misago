from django.contrib.auth import get_user_model
from django.utils.translation import npgettext
from rest_framework import serializers

User = get_user_model()

__all__ = ["ModerateAvatarSerializer"]


class ModerateAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "is_avatar_locked",
            "avatar_lock_user_message",
            "avatar_lock_staff_message",
        ]
