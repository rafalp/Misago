from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.threads.serializers import MovePostsSerializer


def posts_move_endpoint(request, thread, viewmodel):
    if not thread.acl['can_move_posts']:
        raise PermissionDenied(_("You can't move posts in this thread."))

    serializer = MovePostsSerializer(
        data=request.data,
        context={
            'request': request,
            'thread': thread,
            'viewmodel': viewmodel,
        }
    )

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    new_thread = serializer.validated_data['new_thread']

    for post in serializer.validated_data['posts']:
        post.move(new_thread)
        post.save()

    thread.synchronize()
    thread.save()

    new_thread.synchronize()
    new_thread.save()

    thread.category.synchronize()
    thread.category.save()

    if thread.category != new_thread.category:
        new_thread.category.synchronize()
        new_thread.category.save()

    return Response({})
