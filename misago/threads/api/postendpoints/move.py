from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.threads.permissions import allow_move_post, exclude_invisible_posts
from misago.threads.utils import get_thread_id_from_url


MOVE_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


def posts_move_endpoint(request, thread, viewmodel):
    if not thread.acl['can_move_posts']:
        raise PermissionDenied(_("You can't move posts in this thread."))

    try:
        new_thread = clean_thread_for_move(request, thread, viewmodel)
        posts = clean_posts_for_move(request, thread)
    except PermissionDenied as e:
        return Response({'detail': six.text_type(e)}, status=400)

    for post in posts:
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


def clean_thread_for_move(request, thread, viewmodel):
    new_thread_id = get_thread_id_from_url(request, request.data.get('thread_url', None))
    if not new_thread_id:
        raise PermissionDenied(_("This is not a valid thread link."))
    if new_thread_id == thread.pk:
        raise PermissionDenied(_("Thread to move posts to is same as current one."))

    try:
        new_thread = viewmodel(request, new_thread_id, select_for_update=True).unwrap()
    except Http404:
        raise PermissionDenied(
            _(
                "The thread you have entered link to doesn't "
                "exist or you don't have permission to see it."
            )
        )

    if not new_thread.acl['can_reply']:
        raise PermissionDenied(_("You can't move posts to threads you can't reply."))

    return new_thread


def clean_posts_for_move(request, thread):
    try:
        posts_ids = list(map(int, request.data.get('posts', [])))
    except (ValueError, TypeError):
        raise PermissionDenied(_("One or more post ids received were invalid."))

    if not posts_ids:
        raise PermissionDenied(_("You have to specify at least one post to move."))
    elif len(posts_ids) > MOVE_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be moved at single time.",
            "No more than %(limit)s posts can be moved at single time.",
            MOVE_LIMIT,
        )
        raise PermissionDenied(message % {'limit': MOVE_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.select_for_update().filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        post.thread = thread
        allow_move_post(request.user, post)
        posts.append(post)

    if len(posts) != len(posts_ids):
        raise PermissionDenied(_("One or more posts to move could not be found."))

    return posts
