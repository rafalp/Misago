from misago.threads.models import Post
from misago.threads.serializers import PostFeedSerializer


class UserFeedSerializer(PostFeedSerializer):
    class Meta:
        model = Post
        fields = PostFeedSerializer.Meta.fields

        fields.remove('poster')
        fields.remove('poster_name')
