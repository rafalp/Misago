from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.core.utils import clean_ids_list
from misago.threads.moderation import posts as moderation
from misago.threads.permissions import (
    allow_delete_best_answer, allow_delete_event, allow_delete_post)
from misago.threads.permissions import exclude_invisible_posts
from misago.threads.serializers import DeletePostsSerializer


DELETE_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


def delete_post(request, thread, post):
    if post.is_event:
        allow_delete_event(request.user, post)
    else:
        allow_delete_best_answer(request.user, post)
        allow_delete_post(request.user, post)

    moderation.delete_post(request.user, post)

    sync_related(thread)
    return Response({})


def delete_bulk(request, thread):
    serializer = DeletePostsSerializer(
        data={'posts': request.data},
        context={
            'thread': thread,
            'user': request.user,
        },
    )

    if not serializer.is_valid():
        if 'posts' in serializer.errors:
            errors = serializer.errors['posts']
        else:
            errors = list(serializer.errors.values())[0]
        return Response({'detail': errors}, status=400)

    for post in serializer.validated_data['posts']:
        post.delete()

    sync_related(thread)

    return Response({})


def sync_related(thread):
    thread.synchronize()
    thread.save()

    thread.category.synchronize()
    thread.category.save()
