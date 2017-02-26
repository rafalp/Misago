from rest_framework import serializers

from misago.categories.serializers import CategorySerializer
from misago.core.serializers import MutableFields
from misago.threads.models import Post
from misago.users.serializers import UserSerializer

from .post import PostSerializer


__all__ = [
    'FeedSerializer',
]

FeedUserSerializer = UserSerializer.subset_fields('id', 'username', 'avatars', 'absolute_url')

FeedCategorySerializer = CategorySerializer.subset_fields('name', 'css_class', 'absolute_url')


class FeedSerializer(PostSerializer, MutableFields):
    poster = FeedUserSerializer(many=False, read_only=True)
    category = FeedCategorySerializer(many=False, read_only=True)

    thread = serializers.SerializerMethodField()
    top_category = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + ['category', 'thread', 'top_category']

    def get_thread(self, obj):
        return {
            'title': obj.thread.title,
            'url': obj.thread.get_absolute_url(),
        }

    def get_top_category(self, obj):
        try:
            return FeedCategorySerializer(obj.top_category).data
        except AttributeError:
            return None
