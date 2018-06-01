from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.api.serializers import MutableFields

from . import RankSerializer


UserModel = get_user_model()


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

    is_followed = serializers.SerializerMethodField()
    is_blocked = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    real_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = [
            'id',
            'username',
            'slug',
            'email',
            'joined_on',
            'rank',
            'title',
            'avatars',
            'is_avatar_locked',
            'signature',
            'is_signature_locked',
            'followers',
            'following',
            'threads',
            'posts',
            'is_followed',
            'is_blocked',

            'meta',
            'real_name',
            'status',
        ]

    def get_email(self, obj):
        if (obj == self.context['user'] or self.context['user'].acl_cache['can_see_users_emails']):
            return obj.email
        else:
            return None

    def get_is_followed(self, obj):
        if obj.acl['can_follow']:
            return self.context['user'].is_following(obj)
        else:
            return False

    def get_is_blocked(self, obj):
        if obj.acl['can_block']:
            return self.context['user'].is_blocking(obj)
        else:
            return False

    def get_meta(self, obj):
        return {'score': obj.score}

    def get_real_name(self, obj):
        return obj.get_real_name()

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


UserCardSerializer = UserSerializer.subset_fields(
    'id',
    'username',
    'joined_on',
    'rank',
    'title',
    'avatars',
    'followers',
    'threads',
    'posts',
    'real_name',
    'status',
)
