from django.http import HttpRequest

from ..threads.models import Post, Thread
from .hooks import synchronize_category_hook
from .models import Category


def synchronize_category(
    category: Category, commit: bool = True, request: HttpRequest | None = None
):
    synchronize_category_hook(_synchronize_category_action, category, commit, request)


def _synchronize_category_action(
    category: Category, commit: bool = True, request: HttpRequest | None = None
):
    category.threads = Thread.objects.filter(
        category=category, is_hidden=False, is_unapproved=False
    ).count()

    category.posts = Post.objects.filter(
        category=category,
        is_unapproved=False,
        thread__is_hidden=False,
        thread__is_unapproved=False,
    ).count()

    category.unapproved_threads = Thread.objects.filter(
        category=category, is_unapproved=True
    ).count()
    category.unapproved_posts = Post.objects.filter(
        category=category, is_unapproved=True
    ).count()

    last_thread = (
        Thread.objects.filter(category=category, is_hidden=False, is_unapproved=False)
        .order_by("last_post_id")
        .last()
    )

    if last_thread:
        category.last_posted_at = last_thread.last_posted_at
        category.last_thread = last_thread
        category.last_thread_title = last_thread.title
        category.last_thread_slug = last_thread.slug
        category.last_poster_id = last_thread.last_poster_id
        category.last_poster_name = last_thread.last_poster_name
        category.last_poster_slug = last_thread.last_poster_slug
    else:
        category.last_posted_at = None
        category.last_thread = None
        category.last_thread_title = None
        category.last_thread_slug = None
        category.last_poster = None
        category.last_poster_name = None
        category.last_poster_slug = None

    if commit:
        category.save()
