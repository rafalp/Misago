from rest_framework.response import Response

from ....readtracker import poststracker, threadstracker
from ....readtracker.signals import thread_read


def post_read_endpoint(request, thread, post):
    poststracker.make_read_aware(request, post)
    if post.is_new:
        poststracker.save_read(request.user, post)
        if thread.subscription and thread.subscription.last_read_on < post.posted_on:
            thread.subscription.last_read_on = post.posted_on
            thread.subscription.save()

    threadstracker.make_read_aware(request, thread)

    # send signal if post read marked thread as read
    # used in some places, eg. syncing unread thread count
    if post.is_new and thread.is_read:
        thread_read.send(request.user, thread=thread)

    return Response({"thread_is_read": thread.is_read})
