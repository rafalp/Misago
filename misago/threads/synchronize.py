from django.http import HttpRequest

from ..core.utils import slugify
from ..polls.models import Poll
from ..threadupdates.models import ThreadUpdate
from .hooks import synchronize_thread_hook
from .models import Post, Thread


def synchronize_thread(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
):
    synchronize_thread_hook(_synchronize_thread_action, thread, commit, request)


def _synchronize_thread_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
):
    posts = Post.objects.filter(thread=thread)

    thread.replies = max(0, posts.exclude(is_unapproved=True).count() - 1)

    thread.has_updates = ThreadUpdate.objects.filter(thread=thread).exists()
    thread.has_poll = Poll.objects.filter(thread=thread).exists()

    thread.has_unapproved_posts = posts.filter(is_unapproved=True).exists()
    thread.has_hidden_posts = posts.filter(is_hidden=True).exists()

    thread.first_post = posts.select_related("poster").order_by("id").first()
    if thread.replies:
        thread.last_post = posts.exclude(is_unapproved=True).order_by("id").last()
    else:
        thread.last_post = thread.first_post

    thread.started_at = thread.first_post.posted_at
    thread.last_posted_at = thread.last_post.posted_at

    thread.starter = thread.first_post.poster
    thread.last_poster = thread.last_post.poster

    if thread.starter:
        thread.starter_name = thread.starter.username
        thread.starter_slug = thread.starter.slug
    else:
        thread.starter_name = thread.first_post.poster_name
        thread.starter_slug = slugify(thread.first_post.poster_name)

    if thread.last_poster:
        thread.last_poster_name = thread.last_poster.username
        thread.last_poster_slug = thread.last_poster.slug
    else:
        thread.last_poster_name = thread.last_post.poster_name
        thread.last_poster_slug = slugify(thread.last_post.poster_name)

    if thread.solution_id:
        solution = posts.filter(id=thread.solution_id).first()
    else:
        solution = None

    if not solution or solution.thread_id != thread.id:
        thread.solution = None
        thread.solution_posted_at = None
        thread.solution_by = None
        thread.solution_by_name = None
        thread.solution_by_slug = None
        thread.solution_selected_at = None
        thread.solution_selected_by = None
        thread.solution_selected_by_name = None
        thread.solution_selected_by_slug = None
        thread.solution_is_locked = False
        thread.solution_locked_at = None
        thread.solution_locked_by = None
        thread.solution_locked_by_name = None
        thread.solution_locked_by_slug = None

    if commit:
        thread.save()
