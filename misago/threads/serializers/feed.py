from rest_framework import serializers

from misago.api.serializers import MutableFields
from misago.categories.serializers import CategorySerializer
from misago.threads.models import Post
from misago.users.serializers import UserSerializer

from .post import PostSerializer


FeedUserSerializer = UserSerializer.subset_fields(
    'id',
    'username',
    'avatars',
    'title',
    'rank',
)

FeedCategorySerializer = CategorySerializer.subset_fields('name', 'css_class')


class FeedSerializer(PostSerializer, MutableFields):
    poster = FeedUserSerializer(many=False, read_only=True)
    category = FeedCategorySerializer(many=False, read_only=True)

    thread = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + ['category', 'thread']

    def get_thread(self, obj):
        return {
            'title': obj.thread.title,
            'url': obj.thread.get_absolute_url(),
        }


FeedSerializer = FeedSerializer.exclude_fields('is_liked', 'is_new', 'is_read')
