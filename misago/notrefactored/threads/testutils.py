from django.utils import timezone
from misago.threads.models import Thread, Post, Change, Checkpoint

def create_thread(forum):
    thread = Thread()
    thread.forum = forum
    thread.name = 'Test Thread'
    thread.slug = 'test-thread'
    thread.start = timezone.now()
    thread.last = timezone.now()
    thread.save(force_insert=True)
    return thread


def create_post(thread, user):
    now = timezone.now()
    post = Post()
    post.forum = thread.forum
    post.thread = thread
    post.date = now
    post.user = user
    post.user_name = user.username
    post.ip = '127.0.0.1'
    post.agent = 'No matter'
    post.post = 'No matter'
    post.post_preparsed = 'No matter'
    post.save(force_insert=True)
    if not thread.start_post:
        thread.start = now
        thread.start_post = post
        thread.start_poster = user
        thread.start_poster_name = user.username
        thread.start_poster_slug = user.username_slug
    thread.last = now
    thread.last_post = post
    thread.last_poster = user
    thread.last_poster_name = user.username
    thread.last_poster_slug = user.username_slug
    thread.save(force_update=True)
    return post