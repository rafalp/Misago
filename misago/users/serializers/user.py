from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.acl import serialize_acl

from . import RankSerializer


class StatusSerializer(serializers.Serializer):
    is_offline = serializers.BooleanField()
    is_online = serializers.BooleanField()
    is_hidden = serializers.BooleanField()
    is_offline_hidden = serializers.BooleanField()
    is_online_hidden = serializers.BooleanField()
    last_click = serializers.DateTimeField()

    is_banned = serializers.BooleanField()
    banned_until = serializers.DateTimeField()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    rank = RankSerializer(many=False, read_only=True)
    is_followed = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    short_title = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    signature = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    acl = serializers.SerializerMethodField()
    api_url = serializers.SerializerMethodField()

    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = (
            'id',
            'username',
            'slug',
            'joined_on',
            'avatars',
            'title',
            'short_title',
            'rank',
            'signature',
            'threads',
            'posts',
            'followers',
            'following',
            'status',
            'absolute_url',
        )

    def get_email(self, obj):
        if (obj == self.context['user'] or
                self.context['user'].acl['can_see_users_emails']):
            return obj.email
        else:
            return None

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

    def get_meta(self, obj):
        return {'score': obj.score}

    def get_short_title(self, obj):
        return obj.short_title

    def get_signature(self, obj):
        if obj.has_valid_signature:
            return obj.signature_parsed
        else:
            return None

    def get_status(self, obj):
        try:
            return StatusSerializer(obj.status).data
        except AttributeError:
            return None

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_api_url(self, obj):
        return {
            'root': reverse('misago:api:user-detail', kwargs={'pk': obj.pk}),
            'follow': reverse('misago:api:user-follow', kwargs={'pk': obj.pk}),
            'ban': reverse('misago:api:user-ban', kwargs={'pk': obj.pk}),
            'moderate_avatar': reverse(
                'misago:api:user-moderate-avatar', kwargs={'pk': obj.pk}),
            'moderate_username': reverse(
                'misago:api:user-moderate-username', kwargs={'pk': obj.pk}),
            'delete': reverse('misago:api:user-delete', kwargs={'pk': obj.pk}),
            'threads': reverse('misago:api:user-threads', kwargs={'pk': obj.pk}),
            'posts': reverse('misago:api:user-posts', kwargs={'pk': obj.pk}),
        }
