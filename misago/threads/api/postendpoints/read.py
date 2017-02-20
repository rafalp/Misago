from rest_framework.response import Response

from misago.readtracker.threadstracker import make_posts_read_aware, read_thread


def post_read_endpoint(request, thread, post):
    make_posts_read_aware(request.user, thread, [post])
    if not post.is_read:
        read_thread(request.user, thread, post)
        if thread.subscription and thread.subscription.last_read_on < post.posted_on:
            thread.subscription.last_read_on = post.posted_on
            thread.subscription.save()
        return Response({'thread_is_read': thread.last_post_on <= post.posted_on})
    return Response({'thread_is_read': True})
