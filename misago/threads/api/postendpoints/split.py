from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.conf import settings
from misago.threads.models import Thread
from misago.threads.moderation import threads as moderation
from misago.threads.permissions import exclude_invisible_posts
from misago.threads.serializers import NewThreadSerializer


SPLIT_LIMIT = settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL


class SplitError(Exception):
    def __init__(self, msg):
        self.msg = msg


def posts_split_endpoint(request, thread):
    if not thread.acl['can_move_posts']:
        raise PermissionDenied(_("You can't split posts from this thread."))

    try:
        posts = clean_posts_for_split(request, thread)
    except SplitError as e:
        return Response({'detail': e.msg}, status=400)

    serializer = NewThreadSerializer(context=request.user, data=request.data)
    if serializer.is_valid():
        split_posts_to_new_thread(request, thread, serializer.validated_data, posts)
        return Response({})
    else:
        return Response(serializer.errors, status=400)


def clean_posts_for_split(request, thread):
    try:
        posts_ids = list(map(int, request.data.get('posts', [])))
    except (ValueError, TypeError):
        raise SplitError(_("One or more post ids received were invalid."))

    if not posts_ids:
        raise SplitError(_("You have to specify at least one post to split."))
    elif len(posts_ids) > SPLIT_LIMIT:
        message = ungettext(
            "No more than %(limit)s post can be split at single time.",
            "No more than %(limit)s posts can be split at single time.",
            SPLIT_LIMIT,
        )
        raise SplitError(message % {'limit': SPLIT_LIMIT})

    posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)
    posts_queryset = posts_queryset.select_for_update().filter(id__in=posts_ids).order_by('id')

    posts = []
    for post in posts_queryset:
        if post.is_event:
            raise SplitError(_("Events can't be split."))
        if post.pk == thread.first_post_id:
            raise SplitError(_("You can't split thread's first post."))
        if post.is_hidden and not thread.category.acl['can_hide_posts']:
            raise SplitError(_("You can't split posts the content you can't see."))

        posts.append(post)

    if len(posts) != len(posts_ids):
        raise SplitError(_("One or more posts to split could not be found."))

    return posts


def split_posts_to_new_thread(request, thread, validated_data, posts):
    new_thread = Thread(
        category=validated_data['category'],
        started_on=thread.started_on,
        last_post_on=thread.last_post_on,
    )

    new_thread.set_title(validated_data['title'])
    new_thread.save()

    for post in posts:
        post.move(new_thread)
        post.save()

    thread.synchronize()
    thread.save()

    new_thread.synchronize()
    new_thread.save()

    if validated_data.get('weight') == Thread.WEIGHT_GLOBAL:
        moderation.pin_thread_globally(request, new_thread)
    elif validated_data.get('weight'):
        moderation.pin_thread_locally(request, new_thread)
    if validated_data.get('is_hidden', False):
        moderation.hide_thread(request, new_thread)
    if validated_data.get('is_closed', False):
        moderation.close_thread(request, new_thread)

    thread.category.synchronize()
    thread.category.save()

    if new_thread.category != thread.category:
        new_thread.category.synchronize()
        new_thread.category.save()
