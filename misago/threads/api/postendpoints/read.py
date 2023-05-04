from rest_framework.response import Response

from ....notifications.models import Notification, WatchedThread
from ....readtracker import poststracker, threadstracker
from ....readtracker.signals import thread_read
from ....users.models import User
from ...models import Post


def post_read_endpoint(request, thread, watched_thread, post):
    poststracker.make_read_aware(request, post)
    if post.is_new:
        poststracker.save_read(request.user, post)

        update_watched_thread(watched_thread, post)
        read_post_notifications(request.user, post)

    threadstracker.make_read_aware(request, thread)

    # send signal if post read marked thread as read
    # used in some places, eg. syncing unread thread count
    if post.is_new and thread.is_read:
        thread_read.send(request.user, thread=thread)

    return Response({"thread_is_read": thread.is_read})


def update_watched_thread(watched_thread: WatchedThread | None, post: Post):
    if watched_thread and watched_thread.read_at < post.posted_on:
        watched_thread.read_at = post.posted_on
        watched_thread.save(update_fields=["read_at"])


def read_post_notifications(user: User, post: Post):
    updated_notifications = Notification.objects.filter(
        user=user, post=post, is_read=False
    ).update(is_read=True)
    if updated_notifications:
        new_unread_notifications = max(
            [0, user.unread_notifications - updated_notifications]
        )

        if user.unread_notifications != new_unread_notifications:
            user.unread_notifications = new_unread_notifications
            user.save(update_fields=["unread_notifications"])
