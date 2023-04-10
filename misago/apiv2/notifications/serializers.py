from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import serializers

from ...notifications.models import Notification
from ...notifications.messages import message_factory

User = get_user_model()


class NotificationActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "avatars",
            # "url",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["created_at"]

    def to_representation(self, obj: Notification) -> dict:
        data = super().to_representation(obj)

        if obj.actor:
            actor_data = NotificationActorSerializer(obj.actor).data
            actor_data["url"] = obj.actor.get_absolute_url()
        else:
            actor_data = None

        return {
            "id": obj.id,
            "isRead": obj.is_read,
            "createdAt": data["created_at"],
            "actor": actor_data,
            "actorName": obj.actor_name,
            "message": message_factory.get_message(obj),
            "url": reverse("misago:notification", kwargs={"notification_id": obj.id}),
        }
