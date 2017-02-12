from rest_framework import serializers

from django.urls import reverse

from misago.categories.serializers import CategorySerializer
from misago.core.serializers import Subsettable
from misago.threads.models import Post
from misago.users.serializers import BasicUserSerializer

from .post import PostSerializer


__all__ = [
    'FeedSerializer',
]


CategoryFeedSerializer = CategorySerializer.subset(
    'name', 'css_class', 'absolute_url')


class FeedSerializer(PostSerializer, Subsettable):
    poster = BasicUserSerializer(many=False, read_only=True)
    category = CategoryFeedSerializer(many=False, read_only=True)

    thread = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + [
            'category',

            'thread',
            'top_category'
        ]

    def get_thread(self, obj):
        return {
            'title': obj.thread.title,
            'url': obj.thread.get_absolute_url()
        }

    def get_top_category(self, obj):
        try:
            return CategoryFeedSerializer(obj.top_category).data
        except AttributeError:
            return None
