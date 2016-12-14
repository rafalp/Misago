from rest_framework.response import Response

from ...serializers import PostLikeSerializer


def likes_list_endpoint(request, post):
    queryset = post.postlike_set.values(
        'id', 'user_id', 'user_name', 'user_slug', 'liked_on'
    )

    likes = []
    for like in queryset.iterator():
        likes.append(PostLikeSerializer(like).data)

    return Response(likes)
