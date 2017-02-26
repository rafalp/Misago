from rest_framework.response import Response

from misago.threads.serializers import PostLikeSerializer


def likes_list_endpoint(request, post):
    queryset = post.postlike_set.values('id', 'liker_id', 'liker_name', 'liker_slug', 'liked_on')

    likes = []
    for like in queryset.iterator():
        likes.append(PostLikeSerializer(like).data)

    return Response(likes)
