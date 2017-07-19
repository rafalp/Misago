from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.threads.moderation import posts as moderation
from misago.threads.permissions import allow_delete_event, allow_delete_post
from misago.threads.permissions import exclude_invisible_posts


DELETE_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


def delete_post(request, thread, post):
    if post.is_event:
        allow_delete_event(request.user, post)
    else:
        allow_delete_post(request.user, post)

    moderation.delete_post(request.user, post)

    sync_related(thread)
    return Response({})


def delete_bulk(request, thread):
    posts = clean_posts_for_delete(request, thread)

    for post in posts:
        post.delete()

    sync_related(thread)
    return Response({})


def sync_related(thread):
    thread.synchronize()
    thread.save()

    thread.category.synchronize()
    thread.category.save()


def clean_posts_for_delete(request, thread):
    try:
        posts_ids = list(map(int, request.data or []))
    except (ValueError, TypeError):
        raise PermissionDenied(_("One or more post ids received were invalid."))

    if not posts_ids:
        raise PermissionDenied(_("You have to specify at least one post to delete."))
    elif len(posts_ids) > DELETE_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be deleted at single time.",
            "No more than %(limit)s posts can be deleted at single time.",
            DELETE_LIMIT,
        )
        raise PermissionDenied(message % {'limit': DELETE_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        post.thread = thread
        if post.is_event:
            allow_delete_event(request.user, post)
        else:
            allow_delete_post(request.user, post)
        posts.append(post)

    if len(posts) != len(posts_ids):
        raise PermissionDenied(_("One or more posts to delete could not be found."))

    return posts
