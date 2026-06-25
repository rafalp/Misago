from django.db import transaction
from django.http import HttpRequest

from ..attachments.models import Attachment
from ..likes.models import Like
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..postedits.models import PostEdit
from ..postgres.delete import delete_all, delete_one
from ..privatethreads.models import PrivateThreadMember
from ..readtracker.models import ReadThread
from ..threadupdates.models import ThreadUpdate
from .hooks import delete_post_hook, delete_thread_hook
from .models import Post, Thread


@transaction.atomic
def delete_thread(thread: Thread, request: HttpRequest | None = None):
    delete_thread_hook(_delete_thread_action, thread, request)


def _delete_thread_action(thread: Thread, request: HttpRequest | None = None):
    category = thread.category

    if category.last_thread_id == thread.id:
        category.last_thread = None
        category.save(update_fields=["last_thread"])

    thread.first_post = None
    thread.last_post = None
    thread.solution = None
    thread.save(update_fields=["first_post", "last_post", "solution"])

    Attachment.objects.filter(thread=thread).update(
        category=None,
        thread=None,
        post=None,
        is_deleted=True,
    )

    delete_all(PollVote, thread_id=thread.id)
    delete_all(Poll, thread_id=thread.id)

    delete_all(Like, thread_id=thread.id)
    delete_all(Notification, thread_id=thread.id)
    delete_all(PostEdit, thread_id=thread.id)
    delete_all(PrivateThreadMember, thread_id=thread.id)
    delete_all(ReadThread, thread_id=thread.id)
    delete_all(ThreadUpdate, thread_id=thread.id)
    delete_all(WatchedThread, thread_id=thread.id)

    delete_all(Post, thread_id=thread.id)

    delete_one(thread)


@transaction.atomic
def delete_post(post: Post, request: HttpRequest | None = None):
    delete_post_hook(_delete_post_action, post, request)


def _delete_post_action(post: Post, request: HttpRequest | None = None):
    thread = post.thread

    Attachment.objects.filter(post=post).update(
        category=None,
        thread=None,
        post=None,
        is_deleted=True,
    )

    delete_all(Like, post_id=post.id)
    delete_all(Notification, post_id=post.id)
    delete_all(PostEdit, post_id=post.id)

    save_thread_fields = set()
    if thread.first_post_id == post.id:
        thread.first_post = None
        save_thread_fields.add("first_post")
    if thread.last_post_id == post.id:
        thread.last_post = None
        save_thread_fields.add("last_post")
    if thread.solution_id == post.id:
        thread.solution = None
        save_thread_fields.add("solution")
    if save_thread_fields:
        thread.save(update_fields=save_thread_fields)

    delete_one(post)
