from django.contrib.auth import get_user_model

from rest_framework import serializers

from misago.acl import serialize_acl

from misago.users.online.utils import get_user_state
from misago.users.serializers import RankSerializer


__all__ = [
    'AuthenticatedUserSerializer',
    'AnonymousUserSerializer',
    'BasicUserSerializer',
    'UserSerializer',
    'UserProfileSerializer',
]


class AuthenticatedUserSerializer(serializers.ModelSerializer):
    acl = serializers.SerializerMethodField()
    rank = RankSerializer(many=False, read_only=True)

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
            'acl'
        )

    def get_acl(self, obj):
        return serialize_acl(obj)


class AnonymousUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    acl = serializers.SerializerMethodField()

    def get_acl(self, obj):
        return serialize_acl(obj)


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'avatar_hash'
        )


class UserSerializer(serializers.ModelSerializer):
    rank = RankSerializer(many=False, read_only=True)
    state = serializers.SerializerMethodField()
    signature = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'is_avatar_locked',
            'avatar_hash',
            'title',
            'rank',
            'state',
            'is_signature_locked',
            'signature',
        )

    def get_state(self, obj):
        return get_user_state(obj, self.context['user'].acl)

    def get_signature(self, obj):
        if obj.has_valid_signature:
            return obj.signature.signature_parsed
        else:
            return None


class UserProfileSerializer(UserSerializer):
    email = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    acl = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'email',
            'is_avatar_locked',
            'avatar_hash',
            'title',
            'rank',
            'is_signature_locked',
            'signature',
            'is_followed',
            'is_blocked',
            'state',
            'acl',
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
