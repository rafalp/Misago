from rest_framework import serializers

from django.urls import reverse

from misago.categories.serializers import CategorySerializer
from misago.core.serializers import MutableFields
from misago.threads.models import Thread

from .poll import PollSerializer
from .threadparticipant import ThreadParticipantSerializer


__all__ = [
    'ThreadSerializer',
    'PrivateThreadSerializer',
    'ThreadsListSerializer',
]

BasicCategorySerializer = CategorySerializer.subset_fields(
    'id', 'parent', 'name', 'description', 'is_closed', 'css_class',
    'level', 'lft', 'rght', 'is_read', 'api', 'url'
)


class ThreadSerializer(serializers.ModelSerializer, MutableFields):
    category = BasicCategorySerializer(many=False, read_only=True)

    acl = serializers.SerializerMethodField()
    has_unapproved_posts = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    path = BasicCategorySerializer(many=True, read_only=True)
    poll = PollSerializer(many=False, read_only=True)
    subscription = serializers.SerializerMethodField()

    api = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            'id',
            'category',
            'title',
            'replies',
            'has_unapproved_posts',
            'started_on',
            'starter_name',
            'last_post_on',
            'last_post_is_event',
            'last_post',
            'last_poster_name',
            'is_unapproved',
            'is_hidden',
            'is_closed',
            'weight',
            'acl',
            'is_new',
            'is_read',
            'path',
            'poll',
            'subscription',
            'api',
            'url',
        ]

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return {}

    def get_has_unapproved_posts(self, obj):
        try:
            acl = obj.acl
        except AttributeError:
            return False

        return acl.get('can_approve') and obj.has_unapproved_posts

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

    def get_participants(self, obj):
        return ThreadParticipantSerializer(obj.participants_list, many=True).data

    def get_subscription(self, obj):
        try:
            return obj.subscription.send_email
        except AttributeError:
            return None

    def get_api(self, obj):
        return {
            'index': obj.get_api_url(),
            'editor': obj.get_editor_api_url(),
            'merge': obj.get_merge_api_url(),
            'poll': obj.get_poll_api_url(),
            'posts': {
                'index': obj.get_posts_api_url(),
                'merge': obj.get_post_merge_api_url(),
                'move': obj.get_post_move_api_url(),
                'split': obj.get_post_split_api_url(),
            },
        }

    def get_url(self, obj):
        return {
            'index': obj.get_absolute_url(),
            'new_post': obj.get_new_post_url(),
            'last_post': obj.get_last_post_url(),
            'unapproved_post': obj.get_unapproved_post_url(),
            'starter': self.get_starter_url(obj),
            'last_poster': self.get_last_poster_url(obj),
        }

    def get_starter_url(self, obj):
        if obj.starter_id:
            return reverse(
                'misago:user', kwargs={
                    'slug': obj.starter_slug,
                    'pk': obj.starter_id,
                }
            )
        return None

    def get_last_poster_url(self, obj):
        if obj.last_poster_id:
            return reverse(
                'misago:user', kwargs={
                    'slug': obj.last_poster_slug,
                    'pk': obj.last_poster_id,
                }
            )
        return None


class PrivateThreadSerializer(ThreadSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ThreadSerializer.Meta.fields + [
            'participants',
        ]


class ThreadsListSerializer(ThreadSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    last_post = serializers.PrimaryKeyRelatedField(read_only=True)
    starter = serializers.SerializerMethodField()
    last_poster = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ThreadSerializer.Meta.fields + [
            'has_poll',
            'starter',
            'last_poster',
        ]

    def get_starter(self, obj):
        if obj.starter_id:
            return {
                'id': obj.starter_id,
                'avatars': obj.starter.avatars,
            }
        return None

    def get_last_poster(self, obj):
        if obj.last_poster_id:
            return {
                'id': obj.last_poster_id,
                'avatars': obj.last_poster.avatars,
            }
        return None


ThreadsListSerializer = ThreadsListSerializer.exclude_fields('path', 'poll')
