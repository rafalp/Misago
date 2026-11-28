from django.http import HttpRequest

from ..search.threads import threads_search
from .hooks import (
    approve_post_hook,
    approve_thread_hook,
    remove_thread_reply_approval_hook,
    require_thread_reply_approval_hook,
)
from .models import Post, Thread


def approve_thread(
    thread: Thread,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return approve_thread_hook(
        _approve_thread_action, thread, update_search, commit, request
    )


def _approve_thread_action(
    thread: Thread,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not thread.is_unapproved:
        return False

    thread.is_unapproved = False

    if commit:
        thread.save()

    if update_search:
        threads_search.update_thread(thread, {"is_unapproved": False})
        threads_search.bulk_update_thread_posts(thread, {"thread_is_unapproved": False})

    return True


def approve_post(
    post: Post,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    return approve_post_hook(_approve_post_action, post, update_search, commit, request)


def _approve_post_action(
    post: Post,
    update_search: bool = True,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not post.is_unapproved:
        return False

    post.is_unapproved = False

    if commit:
        post.save()

    if update_search:
        threads_search.update_post(post, {"is_unapproved": False})

    return True


def require_thread_reply_approval(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return require_thread_reply_approval_hook(
        _require_thread_reply_approval_action, thread, commit, request
    )


def _require_thread_reply_approval_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if thread.require_reply_approval:
        return False

    thread.require_reply_approval = True

    if commit:
        thread.save()

    return True


def remove_thread_reply_approval(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    return remove_thread_reply_approval_hook(
        _remove_thread_reply_approval_action, thread, commit, request
    )


def _remove_thread_reply_approval_action(
    thread: Thread, commit: bool = True, request: HttpRequest | None = None
) -> bool:
    if not thread.require_reply_approval:
        return False

    thread.require_reply_approval = False

    if commit:
        thread.save()

    return True
