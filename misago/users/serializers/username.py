from django.contrib.auth import get_user_model
from django.utils.translation import pgettext
from rest_framework import serializers

from ..validators import validate_username

User = get_user_model()


class ChangeUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate(self, data):
        username = data.get("username")
        if not username:
            raise serializers.ValidationError(
                pgettext("change username serializer", "Enter new username.")
            )

        user = self.context["user"]
        if username == user.username:
            raise serializers.ValidationError(
                pgettext(
                    "change username serializer", "New username is same as current one."
                )
            )

        settings = self.context["settings"]
        validate_username(settings, username)

        return data

    def change_username(self, changed_by):
        user = self.context["user"]
        user.set_username(self.validated_data["username"], changed_by=changed_by)
        user.save(update_fields=["username", "slug"])
