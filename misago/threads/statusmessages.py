from django.urls import reverse
from typing_extensions import TYPE_CHECKING

from .models import Post, Thread

if TYPE_CHECKING:
    from .views.backend import ViewBackend


def locked_thread_status_message(thread: Thread) -> dict | None:
    if not thread.is_locked:
        return None

    return {
        "id": "locked",
        "template_name": "misago/thread_status_messages/locked.html",
        "locked_at": thread.locked_at,
        "locked_by_id": thread.locked_by_id,
        "locked_by_name": thread.locked_by_name,
        "locked_by_slug": thread.locked_by_slug,
        "lock_reason": thread.lock_reason,
    }


def hidden_thread_status_message(thread: Thread) -> dict | None:
    if not thread.is_hidden:
        return None

    return {
        "id": "hidden",
        "template_name": "misago/thread_status_messages/hidden.html",
        "hidden_at": thread.hidden_at,
        "hidden_by_id": thread.hidden_by_id,
        "hidden_by_name": thread.hidden_by_name,
        "hidden_by_slug": thread.hidden_by_slug,
        "hide_reason": thread.hide_reason,
    }


def unapproved_thread_status_message(thread: Thread) -> dict | None:
    if not thread.is_unapproved:
        return None

    return {
        "id": "unapproved",
        "template_name": "misago/thread_status_messages/unapproved.html",
    }


def require_reply_approval_thread_status_message(thread: Thread) -> dict | None:
    if not thread.require_reply_approval:
        return None

    return {
        "id": "require_reply_approval",
        "template_name": "misago/thread_status_messages/require_reply_approval.html",
    }


def unapproved_posts_thread_status_message(
    thread: Thread, backend: "ViewBackend"
) -> dict | None:
    if not thread.has_unapproved_posts:
        return None

    return {
        "id": "unapproved_posts",
        "template_name": "misago/thread_status_messages/unapproved_posts.html",
        "unapproved_post_url": backend.get_post_unapproved_url(thread),
    }


def locked_post_status_message(post: Post) -> dict | None:
    if not post.is_locked:
        return None

    return {
        "id": "locked",
        "template_name": "misago/post_status_messages/locked.html",
        "locked_at": post.locked_at,
        "locked_by_id": post.locked_by_id,
        "locked_by_name": post.locked_by_name,
        "locked_by_slug": post.locked_by_slug,
        "lock_reason": post.lock_reason,
    }


def hidden_post_status_message(post: Post) -> dict | None:
    if not post.is_hidden:
        return None

    return {
        "id": "hidden",
        "template_name": "misago/post_status_messages/hidden.html",
        "hidden_at": post.hidden_at,
        "hidden_by_id": post.hidden_by_id,
        "hidden_by_name": post.hidden_by_name,
        "hidden_by_slug": post.hidden_by_slug,
        "hide_reason": post.hide_reason,
    }


def unapproved_post_status_message(
    post: Post, message_for_poster: bool = False
) -> dict | None:
    if not post.is_unapproved:
        return None

    return {
        "id": "unapproved",
        "template_name": "misago/post_status_messages/unapproved.html",
        "message_for_poster": message_for_poster,
    }


def solved_post_status_message(post: Post) -> dict | None:
    thread = post.thread

    if not thread.solution_id or thread.first_post_id != post.id:
        return None

    data = {
        "id": "solved",
        "template_name": "misago/post_status_messages/solved.html",
        "solved_at": thread.solution_posted_at,
        "solved_by": None,
        "solved_by_name": thread.solution_by_name,
        "solution_url": reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    }

    if thread.solution_by_id:
        data["solved_by"] = {
            "id": thread.solution_by_id,
            "username": thread.solution_by_name,
            "slug": thread.solution_by_slug,
        }

    return data


def solution_post_status_message(
    post: Post, extra_data: dict | None = None
) -> dict | None:
    thread = post.thread

    if thread.solution_id != post.id:
        return None

    data = {
        "id": "solution",
        "template_name": "misago/post_status_messages/solution.html",
        "selected_at": thread.solution_selected_at,
        "selected_by": None,
        "selected_by_name": thread.solution_selected_by_name,
        "is_locked": thread.solution_is_locked,
        "locked_at": thread.solution_locked_at,
        "locked_by": None,
        "locked_by_name": thread.solution_locked_by_name,
        "lock_url": None,
        "unlock_url": None,
        "clear_url": None,
    }

    if thread.solution_selected_by_id:
        data["selected_by"] = {
            "id": thread.solution_selected_by_id,
            "username": thread.solution_selected_by_name,
            "slug": thread.solution_selected_by_slug,
        }

    if thread.solution_locked_by_id:
        data["locked_by"] = {
            "id": thread.solution_locked_by_id,
            "username": thread.solution_locked_by_name,
            "slug": thread.solution_locked_by_slug,
        }

    if extra_data:
        data.update(extra_data)

    return data
