from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import serializers

from ...acl.useracl import serialize_user_acl
from .user import UserSerializer

User = get_user_model()

__all__ = ["AuthenticatedUserSerializer", "AnonymousUserSerializer"]


class AuthFlags:
    def get_is_authenticated(self, obj):
        return bool(obj.is_authenticated)

    def get_is_anonymous(self, obj):
        return bool(obj.is_anonymous)


class AuthenticatedUserSerializer(UserSerializer, AuthFlags):
    email = serializers.SerializerMethodField()
    is_authenticated = serializers.SerializerMethodField()
    is_anonymous = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + [
            "has_usable_password",
            "is_hiding_presence",
            "limits_private_thread_invites_to",
            "unread_private_threads",
            "watch_started_threads",
            "watch_replied_threads",
            "watch_new_private_threads_by_followed",
            "watch_new_private_threads_by_other_users",
            "notify_new_private_threads_by_followed",
            "notify_new_private_threads_by_other_users",
            "is_authenticated",
            "is_anonymous",
        ]

    def get_acl(self, obj):
        acl = self.context.get("acl")
        if acl:
            return serialize_user_acl(acl)
        return {}

    def get_email(self, obj):
        return obj.email

    def get_api(self, obj):
        return {
            "avatar": reverse("misago:api:user-avatar", kwargs={"pk": obj.pk}),
            "details": reverse("misago:api:user-details", kwargs={"pk": obj.pk}),
            "edit_details": reverse(
                "misago:api:user-edit-details", kwargs={"pk": obj.pk}
            ),
        }

    def to_representation(self, instance) -> dict:
        data = super().to_representation(instance)
        data["unreadNotifications"] = instance.get_unread_notifications_for_display()
        return data


AuthenticatedUserSerializer = AuthenticatedUserSerializer.exclude_fields(
    "is_avatar_locked",
    "is_blocked",
    "is_followed",
    "is_signature_locked",
    "meta",
    "signature",
    "status",
)


class AnonymousUserSerializer(serializers.Serializer, AuthFlags):
    id = serializers.ReadOnlyField()
    acl = serializers.SerializerMethodField()
    is_authenticated = serializers.SerializerMethodField()
    is_anonymous = serializers.SerializerMethodField()

    def get_acl(self, obj):
        acl = self.context.get("acl")
        if acl:
            return serialize_user_acl(acl)
        return {}
