from django.contrib.auth import get_user_model

from rest_framework import serializers

from misago.acl import serialize_acl


__ALL__ = ['AuthenticatedUserSerializer', 'AnonymousUserSerializer']


class AuthenticatedUserSerializer(serializers.ModelSerializer):
    acl = serializers.SerializerMethodField()

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
            'new_notifications',
            'limits_private_thread_invites_to',
            'unread_private_threads',
            'sync_unread_private_threads',
            'subscribe_to_started_threads',
            'subscribe_to_replied_threads',
            'threads',
            'posts',
            'acl')

    def get_acl(self, obj):
        return serialize_acl(obj)


class AnonymousUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    acl = serializers.SerializerMethodField()

    def get_acl(self, obj):
        return serialize_acl(obj)
