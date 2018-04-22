from rest_framework import serializers

from django.urls import reverse

from misago.api.serializers import MutableFields
from misago.threads.models import Post
from misago.users.serializers import UserSerializer as BaseUserSerializer


UserSerializer = BaseUserSerializer.subset_fields(
    'id',
    'username',
    'rank',
    'avatars',
    'signature',
    'title',
    'status',
    'posts',
)


class PostSerializer(serializers.ModelSerializer, MutableFields):
    poster = UserSerializer(many=False, read_only=True)
    poster_ip = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    last_editor = serializers.PrimaryKeyRelatedField(read_only=True)
    hidden_by = serializers.PrimaryKeyRelatedField(read_only=True)

    is_read = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    last_likes = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'poster',
            'poster_name',
            'poster_ip',
            'content',
            'attachments',
            'posted_on',
            'updated_on',
            'hidden_on',
            'edits',
            'last_editor',
            'last_editor_name',
            'last_editor_slug',
            'hidden_by',
            'hidden_by_name',
            'hidden_by_slug',
            'is_unapproved',
            'is_hidden',
            'is_protected',
            'is_event',
            'event_type',
            'event_context',
            'is_liked',
            'is_new',
            'is_read',
            'last_likes',
            'likes',
        ]

    def get_poster_ip(self, obj):
        if self.context['user'].acl_cache['can_see_users_ips']:
            return obj.poster_ip
        else:
            return None

    def get_content(self, obj):
        if obj.is_valid and not obj.is_event and (not obj.is_hidden or obj.acl['can_see_hidden']):
            return obj.content
        else:
            return None

    def get_attachments(self, obj):
        return obj.attachments_cache

    def get_is_liked(self, obj):
        try:
            return obj.is_liked
        except AttributeError:
            return None

    def get_is_new(self, obj):
        try:
            return obj.is_new
        except AttributeError:
            return None

    def get_is_read(self, obj):
        try:
            return obj.is_read
        except AttributeError:
            return None

    def get_last_likes(self, obj):
        if obj.is_event:
            return None

        try:
            if obj.acl['can_see_likes']:
                return obj.last_likes
        except AttributeError:
            return None

    def get_likes(self, obj):
        if obj.is_event:
            return None

        try:
            if obj.acl['can_see_likes']:
                return obj.likes
        except AttributeError:
            return None
