from rest_framework.response import Response

from misago.threads.serializers import PostLikeSerializer


def likes_list_endpoint(request, post):
    queryset = post.postlike_set.select_related('liker').values(
        'id', 'liker_id', 'liker_name', 'liker_slug', 'liked_on', 'liker__avatars')

    likes = []
    for like in queryset.iterator():
        likes.append(PostLikeSerializer(like).data)

    return Response(likes)
