from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _, ungettext

from rest_framework.response import Response

from misago.acl import add_acl

from ...permissions.threads import exclude_invisible_posts
from ...utils import get_thread_id_from_url


MOVE_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


class MoveError(Exception):
    def __init__(self, msg):
        self.msg = msg


def posts_move_endpoint(request, thread, viewmodel):
    if not thread.acl['can_move_posts']:
        raise PermissionDenied(_("You can't move posts in this thread."))

    try:
        new_thread = clean_thread_for_move(request, thread, viewmodel)
        posts = clean_posts_for_move(request, thread)
    except MoveError as e:
        return Response({'detail': e.msg}, status=400)

    for post in posts:
        post.move(thread)
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


def clean_thread_for_move(request, thread):
    new_thread_id = get_thread_id_from_url(request, request.data.get('thread_url', None))
    if not new_thread_id:
        raise MoveError(_("This is not a valid thread link."))
    if new_thread_id == thread.pk:
        raise MoveError(_("You can't move this thread's posts to itself."))

    try:
        new_thread = viewmodel(request, new_thread_id, select_for_update=True).model
    except PermissionDenied as e:
        raise MoveError(e.args[0])
    except Http404:
        raise MoveError(_("The thread you have entered link to doesn't exist or you don't have permission to see it."))

    if not new_thread.acl['can_reply']:
        raise MoveError(_("You don't have permission to move posts to thread you can't reply."))

    return new_thread


def clean_posts_for_move(request, thread):
    try:
        posts_ids = list(map(int, request.data.get('posts', [])))
    except (ValueError, TypeError):
        raise MoveError(_("One or more post ids received were invalid."))

    if len(posts_ids) > MOVE_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be moved at single time.",
            "No more than %(limit)s posts can be moved at single time.",
            MOVE_LIMIT)
        raise MoveError(message % {'limit': MOVE_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.select_for_update().filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        if post.is_event:
            raise MoveError(_("Events can't be moved."))
        if post.pk == thread.first_post_id:
            raise MoveError(_("You can't move first post in thread."))
        if post.is_hidden and not thread.category.acl['can_hide_posts']:
            raise MoveError(_("You can't move posts the content you can't see."))

        posts.append(post)

    if len(posts) != len(posts_ids):
        raise MoveError(_("One or more posts to move could not be found."))

    return posts
