from math import ceil

from django.conf import settings
from django.core.urlresolvers import reverse

from misago.readtracker.threadstracker import make_read_aware

from misago.threads.models import Post


def posts_queryset(qs):
    return qs.count(), qs.order_by('id')


def get_thread_pages(posts):
    if posts <= settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_THREAD_TAIL:
        return 1

    thread_pages = posts / settings.MISAGO_POSTS_PER_PAGE
    thread_tail = posts - thread_pages * settings.MISAGO_POSTS_PER_PAGE
    if thread_tail and thread_tail > settings.MISAGO_THREAD_TAIL:
        thread_pages += 1
    return thread_pages


def get_post_page(posts, post_qs):
    post_no = post_qs.count()
    if posts <= settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_THREAD_TAIL:
        return 1

    thread_pages = get_thread_pages(posts)

    post_page = int(ceil(float(post_no) / settings.MISAGO_POSTS_PER_PAGE))
    if post_page > thread_pages:
        post_page = thread_pages
    return post_page


def hashed_reverse(thread, post, page=1):
    return thread.get_post_url(post.pk, page)


def last(thread, posts_qs):
    posts, qs = posts_queryset(posts_qs)
    thread_pages = get_thread_pages(posts)

    return thread.get_post_url(thread.last_post_id, thread_pages)


def get_post_link(posts, qs, thread, post):
    post_page = get_post_page(posts, qs.filter(id__lte=post.pk))
    return hashed_reverse(thread, post, post_page)


def new(user, thread, posts_qs):
    make_read_aware(user, thread)
    if thread.is_read:
        return last(thread, posts_qs)

    posts, qs = posts_queryset(posts_qs)
    try:
        first_unread = qs.filter(posted_on__gt=thread.last_read_on)[:1][0]
    except IndexError:
        return last(thread, posts_qs)

    return get_post_link(posts, qs, thread, first_unread)


def post(thread, posts_qs, post):
    posts, qs = posts_queryset(posts_qs)
    return get_post_link(posts, qs, thread, post)
