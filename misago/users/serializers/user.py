from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework import serializers

from misago.acl import serialize_acl

from misago.users.serializers import RankSerializer


__all__ = [
    'AuthenticatedUserSerializer',
    'AnonymousUserSerializer',
    'BasicUserSerializer',
    'UserSerializer',
    'ScoredUserSerializer',
    'UserProfileSerializer',
]


class StatusSerializer(serializers.Serializer):
    is_offline = serializers.BooleanField()
    is_online = serializers.BooleanField()
    is_hidden = serializers.BooleanField()
    is_offline_hidden = serializers.BooleanField()
    is_online_hidden = serializers.BooleanField()
    last_click = serializers.DateTimeField()

    is_banned = serializers.BooleanField()
    banned_until = serializers.DateTimeField()


class AuthenticatedUserSerializer(serializers.ModelSerializer):
    acl = serializers.SerializerMethodField()
    rank = RankSerializer(many=False, read_only=True)

    absolute_url = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'email',
            'joined_on',
            'is_hiding_presence',
            'title',
            'full_title',
            'short_title',
            'rank',
            'avatar_hash',
            'new_notifications',
            'limits_private_thread_invites_to',
            'unread_private_threads',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads',
            'threads',
            'posts',
            'followers',
            'following',
            'acl',
            'absolute_url',
            'api_url'
        )

    def get_acl(self, obj):
        return serialize_acl(obj)

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_api_url(self, obj):
        return {
            'avatar': reverse(
                'misago:api:user-avatar', kwargs={'pk': obj.pk}),
            'options': reverse(
                'misago:api:user-forum-options', kwargs={'pk': obj.pk}),
            'username': reverse(
                'misago:api:user-username', kwargs={'pk': obj.pk}),
            'change_email': reverse(
                'misago:api:user-change-email', kwargs={'pk': obj.pk}),
            'change_password': reverse(
                'misago:api:user-change-password', kwargs={'pk': obj.pk}),
        }

class AnonymousUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    acl = serializers.SerializerMethodField()

    def get_acl(self, obj):
        return serialize_acl(obj)


class BaseSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class BasicUserSerializer(BaseSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'avatar_hash',
            'absolute_url',
        )


class UserSerializer(BaseSerializer):
    rank = RankSerializer(many=False, read_only=True)
    status = serializers.SerializerMethodField()
    signature = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'joined_on',
            'avatar_hash',
            'title',
            'rank',
            'signature',
            'threads',
            'posts',
            'followers',
            'following',
            'status',
            'absolute_url',
        )

    def get_status(self, obj):
        try:
            return StatusSerializer(obj.status).data
        except AttributeError:
            return None

    def get_signature(self, obj):
        if obj.has_valid_signature:
            return obj.signature.signature_parsed
        else:
            return None


class ScoredUserSerializer(UserSerializer):
    meta = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'joined_on',
            'avatar_hash',
            'title',
            'rank',
            'signature',
            'threads',
            'posts',
            'followers',
            'following',
            'meta',
            'status',
            'absolute_url',
        )

    def get_meta(self, obj):
        return {'score': obj.score}


class UserProfileSerializer(UserSerializer):
    email = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    acl = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'email',
            'joined_on',
            'is_avatar_locked',
            'avatar_hash',
            'title',
            'rank',
            'signature',
            'is_signature_locked',
            'threads',
            'posts',
            'followers',
            'following',
            'is_followed',
            'is_blocked',
            'status',
            'acl',
            'absolute_url',
            'api_url',
        )

    def get_email(self, obj):
        if (obj == self.context['user'] or
                self.context['user'].acl['can_see_users_emails']):
            return obj.email
        else:
            return None

    def get_acl(self, obj):
        return obj.acl_

    def get_is_followed(self, obj):
        if obj.acl_['can_follow']:
            return self.context['user'].is_following(obj)
        else:
            return False

    def get_is_blocked(self, obj):
        if obj.acl_['can_block']:
            return self.context['user'].is_blocking(obj)
        else:
            return False

    def get_api_url(self, obj):
        return {
            'root': reverse('misago:api:user-detail', kwargs={'pk': obj.pk}),
            'follow': reverse('misago:api:user-follow', kwargs={'pk': obj.pk}),
            'moderate_avatar': reverse(
                'misago:api:user-moderate-avatar',kwargs={'pk': obj.pk}),
            'moderate_username': reverse(
                'misago:api:user-moderate-username',kwargs={'pk': obj.pk}),
            'delete': reverse('misago:api:user-delete', kwargs={'pk': obj.pk}),
        }