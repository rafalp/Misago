from rest_framework import serializers

from django.urls import reverse

from misago.core.serializers import MutableFields
from misago.threads.models import Post
from misago.users.serializers import UserSerializer as BaseUserSerializer


__all__ = ['PostSerializer']

UserSerializer = BaseUserSerializer.subset_fields(
    'id',
    'username',
    'rank',
    'avatars',
    'signature',
    'title',
    'status',
    'posts',
    'url',
)


class PostSerializer(serializers.ModelSerializer, MutableFields):
    poster = UserSerializer(many=False, read_only=True)
    poster_ip = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    last_editor = serializers.PrimaryKeyRelatedField(read_only=True)
    hidden_by = serializers.PrimaryKeyRelatedField(read_only=True)

    acl = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    last_likes = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    api = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

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
            'acl',
            'is_liked',
            'is_new',
            'is_read',
            'last_likes',
            'likes',
            'api',
            'url',
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

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return None

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

    def get_api(self, obj):
        api_links = {
            'index': obj.get_api_url(),
            'likes': obj.get_likes_api_url(),
            'editor': obj.get_editor_api_url(),
            'edits': obj.get_edits_api_url(),
            'read': obj.get_read_api_url(),
        }

        if obj.is_event:
            del api_links['likes']

        return api_links

    def get_url(self, obj):
        return {
            'index': obj.get_absolute_url(),
            'last_editor': self.get_last_editor_url(obj),
            'hidden_by': self.get_hidden_by_url(obj),
        }

    def get_last_editor_url(self, obj):
        if obj.last_editor_id:
            return reverse(
                'misago:user', kwargs={
                    'pk': obj.last_editor_id,
                    'slug': obj.last_editor_slug,
                }
            )
        else:
            return None

    def get_hidden_by_url(self, obj):
        if obj.hidden_by_id:
            return reverse(
                'misago:user', kwargs={
                    'pk': obj.hidden_by_id,
                    'slug': obj.hidden_by_slug,
                }
            )
        else:
            return None
