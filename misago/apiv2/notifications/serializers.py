from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...notifications.models import Notification
from ...notifications.registry import registry

User = get_user_model()


class NotificationActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "avatars",
        ]

    def to_representation(self, obj: User) -> dict:
        data = super().to_representation(obj)
        data["url"] = obj.get_absolute_url()
        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["created_at"]

    def to_representation(self, obj: Notification) -> dict:
        data = super().to_representation(obj)

        if obj.actor:
            actor_data = NotificationActorSerializer(obj.actor).data
        else:
            actor_data = None

        return {
            "id": obj.id,
            "isRead": obj.is_read,
            "createdAt": data["created_at"],
            "actor": actor_data,
            "actorName": obj.actor_name,
            "message": registry.get_message(obj),
            "url": obj.get_absolute_url(),
        }
