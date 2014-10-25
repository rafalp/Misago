from math import ceil

from django.core.urlresolvers import reverse

from misago.readtracker.threadstracker import make_read_aware

from misago.threads.models import Post
from misago.threads.permissions import exclude_invisible_posts


def posts_queryset(user, thread):
    qs = exclude_invisible_posts(thread.post_set, user, thread.forum)
    return qs.count(), qs.order_by('id')


def get_thread_pages(posts):
    if posts <= 13:
        return 1

    thread_pages = posts / 10
    thread_tail = posts - thread_pages * 10
    if thread_tail and thread_tail > 3:
        thread_pages += 1
    return thread_pages


def get_post_page(posts, post_qs):
    post_no = post_qs.count()
    if posts <= 13:
        return 1

    thread_pages = get_thread_pages(posts)

    post_page = int(ceil(float(post_no) / 10))
    if post_page > thread_pages:
        post_page = thread_pages
    return post_page


def hashed_reverse(thread, post, page=1):
    link_name = thread.get_url_name()

    if page > 1:
        post_url = reverse(link_name, kwargs={
            'thread_id': thread.id,
            'thread_slug': thread.slug,
            'page': page
        })
    else:
        post_url = reverse(link_name, kwargs={
            'thread_id': thread.id,
            'thread_slug': thread.slug
        })

    return '%s#post-%s' % (post_url, post.pk)


def last(user, thread):
    posts, qs = posts_queryset(user, thread)
    thread_pages = get_thread_pages(posts)

    link_name = thread.get_url_name()
    if thread_pages > 1:
        post_url = reverse(link_name, kwargs={
            'thread_id': thread.id,
            'thread_slug': thread.slug,
            'page': thread_pages
        })
    else:
        post_url = reverse(link_name, kwargs={
            'thread_id': thread.id,
            'thread_slug': thread.slug
        })

    return '%s#post-%s' % (post_url, thread.last_post_id)


def get_post_link(posts, qs, thread, post):
    post_page = get_post_page(posts, qs.filter(id__lte=post.pk))
    return hashed_reverse(thread, post, post_page)


def new(user, thread):
    make_read_aware(user, thread)
    if thread.is_read:
        return last(user, thread)

    posts, qs = posts_queryset(user, thread)
    try:
        first_unread = qs.filter(posted_on__gt=thread.last_read_on)[:1][0]
    except IndexError:
        return last(user, thread)

    return get_post_link(posts, qs, thread, first_unread)


def post(user, thread, post):
    posts, qs = posts_queryset(user, thread)
    return get_post_link(posts, qs, thread, post)
