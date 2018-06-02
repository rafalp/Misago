from rest_framework import serializers

from django.urls import reverse

from misago.api.serializers import MutableFields
from misago.categories.serializers import BasicCategorySerializer
from misago.threads.models import Thread

from .poll import PollSerializer
from .threadparticipant import ThreadParticipantSerializer


class ThreadSerializer(serializers.ModelSerializer, MutableFields):
    category = BasicCategorySerializer(many=False, read_only=True)

    has_unapproved_posts = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()
    path = BasicCategorySerializer(many=True, read_only=True)
    poll = PollSerializer(many=False, read_only=True)
    best_answer = serializers.PrimaryKeyRelatedField(read_only=True)
    best_answer_marked_by = serializers.PrimaryKeyRelatedField(read_only=True)
    subscription = serializers.SerializerMethodField()

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
            'best_answer',
            'best_answer_is_protected',
            'best_answer_marked_on',
            'best_answer_marked_by',
            'best_answer_marked_by_name',
            'best_answer_marked_by_slug',
            'is_new',
            'is_read',
            'path',
            'poll',
            'subscription',
        ]

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


class PrivateThreadSerializer(ThreadSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ThreadSerializer.Meta.fields + ['participants']


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
        if obj.starter:
            avatars = obj.starter.avatars
            real_name = obj.starter.get_real_name()
        else:
            avatars = None
            real_name = None

        return {
            'id': obj.starter_id,
            'username': obj.starter_name,
            'slug': obj.starter_slug,
            'real_name': real_name,
            'avatars': avatars,
        }

    def get_last_poster(self, obj):
        if obj.last_poster:
            avatars = obj.last_poster.avatars
            real_name = obj.last_poster.get_real_name()
        else:
            avatars = None
            real_name = None

        return {
            'id': obj.last_poster_id,
            'username': obj.last_poster_name,
            'slug': obj.last_poster_slug,
            'real_name': real_name,
            'avatars': avatars,
        }



ThreadsListSerializer = ThreadsListSerializer.exclude_fields('path', 'poll')
