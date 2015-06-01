from django.contrib.auth import get_user_model

from rest_framework import serializers

from misago.acl import serialize_acl

from misago.users.serializers import RankSerializer

__all__ = [
    'AuthenticatedUserSerializer',
    'AnonymousUserSerializer',
    'BasicUserSerializer',
    'UserSerializer',
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
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'slug',
            'avatar_hash'
        )
