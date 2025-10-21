from django.http import HttpRequest

from ..polls.models import Poll
from ..core.utils import slugify
from .hooks import synchronize_thread_hook
from .models import Thread


def synchronize_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
):
    replies = max(0, thread.post_set.exclude(is_unapproved=True).count() - 1)

    has_poll = Poll.objects.filter(thread=thread).exists()

    has_reported_posts = False
    has_open_reports = False
    has_unapproved_posts = thread.post_set.filter(is_unapproved=True).exists()
    has_hidden_posts = thread.post_set.filter(is_hidden=True).exists()

    first_post = thread.post_set.select_related("poster").order_by("id").first()
    if replies:
        last_post = thread.post_set.exclude(is_unapproved=True).order_by("id").last()
    else:
        last_post = first_post

    starter = first_post.poster
    last_poster = last_post.poster

    data = {
        "replies": replies,
        "has_poll": has_poll,
        "has_reported_posts": has_reported_posts,
        "has_open_reports": has_open_reports,
        "has_unapproved_posts": has_unapproved_posts,
        "has_hidden_posts": has_hidden_posts,
        "started_at": first_post.posted_at,
        "last_posted_at": last_post.posted_at,
        "first_post": first_post,
        "starter": starter,
        "last_post": last_post,
        "last_poster": last_poster,
    }

    if starter:
        data["starter_name"] = starter.username
        data["starter_slug"] = starter.slug
    else:
        data["starter_name"] = first_post.poster_name
        data["starter_slug"] = slugify(first_post.poster_name)

    if last_poster:
        data["last_poster_name"] = last_poster.username
        data["last_poster_slug"] = last_poster.slug
    else:
        data["last_poster_name"] = last_post.poster_name
        data["last_poster_slug"] = slugify(last_post.poster_name)

    synchronize_thread_hook(
        _synchronize_thread_action,
        thread,
        data,
        commit,
        request,
    )


def _synchronize_thread_action(
    thread: Thread, data: dict, commit: bool = True, request: HttpRequest | None = None
):
    for name, value in data.items():
        setattr(thread, name, value)

    if commit:
        thread.save(update_fields=data.keys())
