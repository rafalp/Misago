from django.core.urlresolvers import reverse

from rest_framework import serializers

from misago.users.serializers import UserSerializer

from ..models import Post


__all__ = [
    'PostSerializer',
    'ThreadPostSerializer',
]


class PostSerializer(serializers.ModelSerializer):
    poster = UserSerializer(many=False, read_only=True)
    parsed = serializers.SerializerMethodField()
    attachments_cache = serializers.SerializerMethodField()
    last_editor = UserSerializer(many=False, read_only=True)
    last_editor_id = serializers.SerializerMethodField()
    last_editor_url = serializers.SerializerMethodField()
    hidden_by = UserSerializer(many=False, read_only=True)
    hidden_by_id = serializers.SerializerMethodField()
    hidden_by_url = serializers.SerializerMethodField()
    acl = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
        )

    def get_parsed(self, obj):
        if obj.is_valid and not obj.is_event and (not obj.is_hidden or obj.acl['can_see_hidden']):
            return obj.parsed
        else:
            return None

    def get_attachments_cache(self, obj):
        # TODO: check if user can download attachments before we'll expose them here
        return None

    def get_last_editor_id(self, obj):
        return obj.last_editor_id

    def get_last_editor_url(self, obj):
        if obj.last_editor_id:
            return reverse('misago:user', kwargs={
                'pk': obj.last_editor_id,
                'slug': obj.last_editor_slug
            })
        else:
            return None

    def get_hidden_by_id(self, obj):
        return obj.hidden_by_id

    def get_hidden_by_url(self, obj):
        if obj.hidden_by:
            return reverse('misago:user', kwargs={
                'pk': obj.hidden_by_id,
                'slug': obj.hidden_by_slug
            })
        else:
            return None

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return None


class ThreadPostSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'poster',
            'poster_name',
            'poster_ip',
            'parsed',
            'has_attachments',
            'attachments_cache',
            'posted_on',
            'updated_on',
            'hidden_on',
            'edits',
            'last_editor_id',
            'last_editor_name',
            'last_editor_slug',
            'last_editor_url',
            'hidden_by_id',
            'hidden_by_name',
            'hidden_by_slug',
            'hidden_by_url',
            'is_unapproved',
            'is_hidden',
            'is_protected',
            'is_event',
            'event_type',
            'event_context',
            'acl',
        )
