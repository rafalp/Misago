from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import serializers

from . import RankSerializer
from ...core.serializers import MutableFields

User = get_user_model()

__all__ = ["StatusSerializer", "UserSerializer", "UserCardSerializer"]


class StatusSerializer(serializers.Serializer):
    is_offline = serializers.BooleanField()
    is_online = serializers.BooleanField()
    is_hidden = serializers.BooleanField()
    is_offline_hidden = serializers.BooleanField()
    is_online_hidden = serializers.BooleanField()
    last_click = serializers.DateTimeField()

    is_banned = serializers.BooleanField()
    banned_until = serializers.DateTimeField()


class UserSerializer(serializers.ModelSerializer, MutableFields):
    email = serializers.SerializerMethodField()
    rank = RankSerializer(many=False, read_only=True)
    signature = serializers.SerializerMethodField()

    acl = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    real_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    api = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "slug",
            "email",
            "joined_on",
            "rank",
            "title",
            "avatars",
            "is_avatar_locked",
            "signature",
            "is_signature_locked",
            "followers",
            "following",
            "threads",
            "posts",
            "acl",
            "is_followed",
            "is_blocked",
            "meta",
            "real_name",
            "status",
            "api",
            "url",
        ]

    def get_acl(self, obj):
        return obj.acl

    def get_email(self, obj):
        request = self.context["request"]
        if obj == request.user or request.user_acl["can_see_users_emails"]:
            return obj.email

    def get_is_followed(self, obj):
        request = self.context["request"]
        if obj.acl["can_follow"]:
            return request.user.is_following(obj)
        return False

    def get_is_blocked(self, obj):
        request = self.context["request"]
        if obj.acl["can_block"]:
            return request.user.is_blocking(obj)
        return False

    def get_meta(self, obj):
        return {"score": obj.score}

    def get_real_name(self, obj):
        return obj.get_real_name()

    def get_signature(self, obj):
        if obj.has_valid_signature:
            return obj.signature_parsed

    def get_status(self, obj):
        try:
            return StatusSerializer(obj.status).data
        except AttributeError:
            return None

    def get_api(self, obj):
        return {
            "index": reverse("misago:api:user-detail", kwargs={"pk": obj.pk}),
            "follow": reverse("misago:api:user-follow", kwargs={"pk": obj.pk}),
            "ban": reverse("misago:api:user-ban", kwargs={"pk": obj.pk}),
            "details": reverse("misago:api:user-details", kwargs={"pk": obj.pk}),
            "edit_details": reverse(
                "misago:api:user-edit-details", kwargs={"pk": obj.pk}
            ),
            "moderate_avatar": reverse(
                "misago:api:user-moderate-avatar", kwargs={"pk": obj.pk}
            ),
            "moderate_username": reverse(
                "misago:api:user-moderate-username", kwargs={"pk": obj.pk}
            ),
            "delete": reverse("misago:api:user-delete", kwargs={"pk": obj.pk}),
            "followers": reverse("misago:api:user-followers", kwargs={"pk": obj.pk}),
            "follows": reverse("misago:api:user-follows", kwargs={"pk": obj.pk}),
            "threads": reverse("misago:api:user-threads", kwargs={"pk": obj.pk}),
            "posts": reverse("misago:api:user-posts", kwargs={"pk": obj.pk}),
        }

    def get_url(self, obj):
        return obj.get_absolute_url()


UserCardSerializer = UserSerializer.subset_fields(
    "id",
    "username",
    "joined_on",
    "rank",
    "title",
    "avatars",
    "followers",
    "threads",
    "posts",
    "real_name",
    "status",
    "url",
)
