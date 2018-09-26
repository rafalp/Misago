from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.threads.serializers import MergePostsSerializer, PostSerializer


def posts_merge_endpoint(request, thread):
    if not thread.acl['can_merge_posts']:
        raise PermissionDenied(_("You can't merge posts in this thread."))

    serializer = MergePostsSerializer(
        data=request.data,
        context={
            'thread': thread,
            'user': request.user,
        },
    )

    if not serializer.is_valid():
        return Response(
            {
                'detail': list(serializer.errors.values())[0],
            },
            status=400,
        )

    posts = serializer.validated_data['posts']
    first_post, merged_posts = posts[0], posts[1:]

    for post in merged_posts:
        post.merge(first_post)
        post.delete()

    if first_post.pk == thread.first_post_id:
        first_post.set_search_document(thread.title)
    else:
        first_post.set_search_document()

    first_post.save()

    first_post.update_search_vector()
    first_post.save(update_fields=['search_vector'])

    first_post.postread_set.all().delete()

    thread.synchronize()
    thread.save()

    thread.category.synchronize()
    thread.category.save()

    first_post.thread = thread
    first_post.category = thread.category

    add_acl(request.user, first_post)

    return Response(PostSerializer(first_post, context={'user': request.user}).data)
