from django.urls import reverse
from django.utils import timezone

from ...solutions.lock import lock_thread_solution
from ...solutions.select import select_thread_solution
from ..statusmessages import (
    hidden_post_status_message,
    hidden_thread_status_message,
    locked_post_status_message,
    locked_thread_status_message,
    require_reply_approval_thread_status_message,
    solution_post_status_message,
    solved_post_status_message,
    unapproved_post_status_message,
    unapproved_posts_thread_status_message,
    unapproved_thread_status_message,
)
from ..views.backend import thread_backend


def test_locked_thread_status_message_returns_none_for_unlocked_thread(thread):
    message = locked_thread_status_message(thread)
    assert message is None


def test_locked_thread_status_message_returns_message_for_locked_thread(thread):
    thread.is_locked = True

    message = locked_thread_status_message(thread)

    assert message == {
        "id": "locked",
        "template_name": "misago/thread_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": None,
        "locked_by_name": None,
        "locked_by_slug": None,
        "lock_reason": None,
    }


def test_locked_thread_status_message_returns_message_for_locked_thread_with_locked_at(
    thread,
):
    thread.is_locked = True
    thread.locked_at = timezone.now()

    message = locked_thread_status_message(thread)

    assert message == {
        "id": "locked",
        "template_name": "misago/thread_status_messages/locked.html",
        "locked_at": thread.locked_at,
        "locked_by_id": None,
        "locked_by_name": None,
        "locked_by_slug": None,
        "lock_reason": None,
    }


def test_locked_thread_status_message_returns_message_for_thread_locked_by_user(
    thread, user
):
    thread.is_locked = True
    thread.locked_by = user
    thread.locked_by_name = user.username
    thread.locked_by_slug = user.slug

    message = locked_thread_status_message(thread)

    assert message == {
        "id": "locked",
        "template_name": "misago/thread_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": user.id,
        "locked_by_name": user.username,
        "locked_by_slug": user.slug,
        "lock_reason": None,
    }


def test_locked_thread_status_message_returns_message_for_thread_locked_by_deleted_user(
    thread,
):
    thread.is_locked = True
    thread.locked_by_name = "User"
    thread.locked_by_slug = "user"

    message = locked_thread_status_message(thread)

    assert message == {
        "id": "locked",
        "template_name": "misago/thread_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": None,
        "locked_by_name": "User",
        "locked_by_slug": "user",
        "lock_reason": None,
    }


def test_locked_thread_status_message_returns_message_for_thread_locked_with_reason(
    thread,
):
    thread.is_locked = True
    thread.lock_reason = "Lorem ipsum"

    message = locked_thread_status_message(thread)

    assert message == {
        "id": "locked",
        "template_name": "misago/thread_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": None,
        "locked_by_name": None,
        "locked_by_slug": None,
        "lock_reason": "Lorem ipsum",
    }


def test_hidden_thread_status_message_returns_none_for_unhidden_thread(thread):
    message = hidden_thread_status_message(thread)
    assert message is None


def test_hidden_thread_status_message_returns_message_for_hidden_thread(thread):
    thread.is_hidden = True

    message = hidden_thread_status_message(thread)

    assert message == {
        "id": "hidden",
        "template_name": "misago/thread_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": None,
        "hidden_by_name": None,
        "hidden_by_slug": None,
        "hide_reason": None,
    }


def test_hidden_thread_status_message_returns_message_for_hidden_thread_with_hidden_at(
    thread,
):
    thread.is_hidden = True
    thread.hidden_at = timezone.now()

    message = hidden_thread_status_message(thread)

    assert message == {
        "id": "hidden",
        "template_name": "misago/thread_status_messages/hidden.html",
        "hidden_at": thread.hidden_at,
        "hidden_by_id": None,
        "hidden_by_name": None,
        "hidden_by_slug": None,
        "hide_reason": None,
    }


def test_hidden_thread_status_message_returns_message_for_thread_hidden_by_user(
    thread, user
):
    thread.is_hidden = True
    thread.hidden_by = user
    thread.hidden_by_name = user.username
    thread.hidden_by_slug = user.slug

    message = hidden_thread_status_message(thread)

    assert message == {
        "id": "hidden",
        "template_name": "misago/thread_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": user.id,
        "hidden_by_name": user.username,
        "hidden_by_slug": user.slug,
        "hide_reason": None,
    }


def test_hidden_thread_status_message_returns_message_for_thread_hidden_by_deleted_user(
    thread,
):
    thread.is_hidden = True
    thread.hidden_by_name = "User"
    thread.hidden_by_slug = "user"

    message = hidden_thread_status_message(thread)

    assert message == {
        "id": "hidden",
        "template_name": "misago/thread_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": None,
        "hidden_by_name": "User",
        "hidden_by_slug": "user",
        "hide_reason": None,
    }


def test_hidden_thread_status_message_returns_message_for_thread_hidden_with_reason(
    thread,
):
    thread.is_hidden = True
    thread.hide_reason = "Lorem ipsum"

    message = hidden_thread_status_message(thread)

    assert message == {
        "id": "hidden",
        "template_name": "misago/thread_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": None,
        "hidden_by_name": None,
        "hidden_by_slug": None,
        "hide_reason": "Lorem ipsum",
    }


def test_unapproved_thread_status_message_returns_none_for_approved_thread(thread):
    message = unapproved_thread_status_message(thread)
    assert message is None


def test_unapproved_thread_status_message_returns_message_for_unapproved_thread(thread):
    thread.is_unapproved = True

    message = unapproved_thread_status_message(thread)

    assert message == {
        "id": "unapproved",
        "template_name": "misago/thread_status_messages/unapproved.html",
    }


def test_require_reply_approval_thread_status_message_returns_none_for_thread_without_reply_approval(
    thread,
):
    message = require_reply_approval_thread_status_message(thread)
    assert message is None


def test_require_reply_approval_thread_status_message_returns_message_for_thread_with_reply_approval(
    thread,
):
    thread.require_reply_approval = True

    message = require_reply_approval_thread_status_message(thread)

    assert message == {
        "id": "require_reply_approval",
        "template_name": "misago/thread_status_messages/require_reply_approval.html",
    }


def test_unapproved_posts_thread_status_message_returns_none_for_thread_without_unapproved_posts(
    thread,
):
    thread.has_unapproved_posts = True

    message = unapproved_posts_thread_status_message(thread, thread_backend)

    assert message == {
        "id": "unapproved_posts",
        "template_name": "misago/thread_status_messages/unapproved_posts.html",
        "unapproved_post_url": reverse(
            "misago:thread-post-unapproved",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    }


def test_locked_post_status_message_returns_none_for_unlocked_post(post):
    message = locked_post_status_message(post)
    assert message is None


def test_locked_post_status_message_returns_message_for_locked_post(post):
    post.is_locked = True

    message = locked_post_status_message(post)

    assert message == {
        "id": "locked",
        "template_name": "misago/post_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": None,
        "locked_by_name": None,
        "locked_by_slug": None,
        "lock_reason": None,
    }


def test_locked_post_status_message_returns_message_for_locked_post_with_locked_at(
    post,
):
    post.is_locked = True
    post.locked_at = timezone.now()

    message = locked_post_status_message(post)

    assert message == {
        "id": "locked",
        "template_name": "misago/post_status_messages/locked.html",
        "locked_at": post.locked_at,
        "locked_by_id": None,
        "locked_by_name": None,
        "locked_by_slug": None,
        "lock_reason": None,
    }


def test_locked_post_status_message_returns_message_for_post_locked_by_user(post, user):
    post.is_locked = True
    post.locked_by = user
    post.locked_by_name = user.username
    post.locked_by_slug = user.slug

    message = locked_post_status_message(post)

    assert message == {
        "id": "locked",
        "template_name": "misago/post_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": user.id,
        "locked_by_name": user.username,
        "locked_by_slug": user.slug,
        "lock_reason": None,
    }


def test_locked_post_status_message_returns_message_for_post_locked_by_deleted_user(
    post,
):
    post.is_locked = True
    post.locked_by_name = "User"
    post.locked_by_slug = "user"

    message = locked_post_status_message(post)

    assert message == {
        "id": "locked",
        "template_name": "misago/post_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": None,
        "locked_by_name": "User",
        "locked_by_slug": "user",
        "lock_reason": None,
    }


def test_locked_post_status_message_returns_message_for_post_locked_with_reason(post):
    post.is_locked = True
    post.lock_reason = "Lorem ipsum"

    message = locked_post_status_message(post)

    assert message == {
        "id": "locked",
        "template_name": "misago/post_status_messages/locked.html",
        "locked_at": None,
        "locked_by_id": None,
        "locked_by_name": None,
        "locked_by_slug": None,
        "lock_reason": "Lorem ipsum",
    }


def test_hidden_post_status_message_returns_none_for_unhidden_post(post):
    message = hidden_post_status_message(post)
    assert message is None


def test_hidden_post_status_message_returns_message_for_hidden_post(post):
    post.is_hidden = True

    message = hidden_post_status_message(post)

    assert message == {
        "id": "hidden",
        "template_name": "misago/post_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": None,
        "hidden_by_name": None,
        "hidden_by_slug": None,
        "hide_reason": None,
    }


def test_hidden_post_status_message_returns_message_for_hidden_post_with_hidden_at(
    post,
):
    post.is_hidden = True
    post.hidden_at = timezone.now()

    message = hidden_post_status_message(post)

    assert message == {
        "id": "hidden",
        "template_name": "misago/post_status_messages/hidden.html",
        "hidden_at": post.hidden_at,
        "hidden_by_id": None,
        "hidden_by_name": None,
        "hidden_by_slug": None,
        "hide_reason": None,
    }


def test_hidden_post_status_message_returns_message_for_post_hidden_by_user(post, user):
    post.is_hidden = True
    post.hidden_by = user
    post.hidden_by_name = user.username
    post.hidden_by_slug = user.slug

    message = hidden_post_status_message(post)

    assert message == {
        "id": "hidden",
        "template_name": "misago/post_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": user.id,
        "hidden_by_name": user.username,
        "hidden_by_slug": user.slug,
        "hide_reason": None,
    }


def test_hidden_post_status_message_returns_message_for_post_hidden_by_deleted_user(
    post,
):
    post.is_hidden = True
    post.hidden_by_name = "User"
    post.hidden_by_slug = "user"

    message = hidden_post_status_message(post)

    assert message == {
        "id": "hidden",
        "template_name": "misago/post_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": None,
        "hidden_by_name": "User",
        "hidden_by_slug": "user",
        "hide_reason": None,
    }


def test_hidden_post_status_message_returns_message_for_post_hidden_with_reason(post):
    post.is_hidden = True
    post.hide_reason = "Lorem ipsum"

    message = hidden_post_status_message(post)

    assert message == {
        "id": "hidden",
        "template_name": "misago/post_status_messages/hidden.html",
        "hidden_at": None,
        "hidden_by_id": None,
        "hidden_by_name": None,
        "hidden_by_slug": None,
        "hide_reason": "Lorem ipsum",
    }


def test_unapproved_post_status_message_returns_none_for_approved_post(post):
    message = unapproved_post_status_message(post)
    assert message is None


def test_unapproved_post_status_message_returns_message_for_unapproved_post(post):
    post.is_unapproved = True

    message = unapproved_post_status_message(post)

    assert message == {
        "id": "unapproved",
        "template_name": "misago/post_status_messages/unapproved.html",
        "message_for_poster": False,
    }


def test_unapproved_post_status_message_returns_message_for_poster_unapproved_post(
    post,
):
    post.is_unapproved = True

    message = unapproved_post_status_message(post, message_for_poster=True)

    assert message == {
        "id": "unapproved",
        "template_name": "misago/post_status_messages/unapproved.html",
        "message_for_poster": True,
    }


def test_solved_post_status_message_returns_none_for_first_post_in_thread_without_solution(
    post,
):
    message = solved_post_status_message(post)
    assert message is None


def test_solved_post_status_message_returns_message_for_first_post_in_thread_with_solution_by_user(
    thread_reply_factory, user, thread, post
):
    solution = thread_reply_factory(thread, poster=user)
    select_thread_solution(thread, solution, "Moderator")

    message = solved_post_status_message(post)

    assert message == {
        "id": "solved",
        "template_name": "misago/post_status_messages/solved.html",
        "solved_at": thread.solution_posted_at,
        "solved_by": {
            "id": user.id,
            "username": user.username,
            "slug": user.slug,
        },
        "solved_by_name": user.username,
        "solution_url": reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    }


def test_solved_post_status_message_returns_message_for_first_post_in_thread_with_solution_by_deleted_user(
    thread_reply_factory, thread, post
):
    solution = thread_reply_factory(thread, poster="OtherUser")
    select_thread_solution(thread, solution, "Moderator")

    message = solved_post_status_message(post)

    assert message == {
        "id": "solved",
        "template_name": "misago/post_status_messages/solved.html",
        "solved_at": thread.solution_posted_at,
        "solved_by": None,
        "solved_by_name": "OtherUser",
        "solution_url": reverse(
            "misago:thread-post-solution",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    }


def test_solved_post_status_message_returns_none_for_other_post_in_thread_with_solution(
    thread_reply_factory, user, thread, reply
):
    solution = thread_reply_factory(thread, poster=user)
    select_thread_solution(thread, solution, "Moderator")

    message = solved_post_status_message(reply)
    assert message is None


def test_solution_post_status_message_returns_none_for_post_in_thread_without_solution(
    reply,
):
    message = solution_post_status_message(reply)
    assert message is None


def test_solution_post_status_message_returns_none_for_post_in_thread_with_solution(
    thread_reply_factory, thread, reply
):
    solution = thread_reply_factory(thread, poster="OtherUser")
    select_thread_solution(thread, solution, "Moderator")

    message = solution_post_status_message(reply)
    assert message is None


def test_solution_post_status_message_returns_message_for_solution_in_thread_selected_by_user(
    thread_reply_factory, user, thread
):
    solution = thread_reply_factory(thread, poster="OtherUser")
    select_thread_solution(thread, solution, user)

    message = solution_post_status_message(solution)

    assert message == {
        "id": "solution",
        "template_name": "misago/post_status_messages/solution.html",
        "selected_at": thread.solution_selected_at,
        "selected_by": {
            "id": user.id,
            "username": user.username,
            "slug": user.slug,
        },
        "selected_by_name": user.username,
        "is_locked": False,
        "locked_at": None,
        "locked_by": None,
        "locked_by_name": None,
        "lock_url": None,
        "unlock_url": None,
        "clear_url": None,
    }


def test_solution_post_status_message_returns_message_for_solution_in_thread_selected_by_deleted_user(
    thread_reply_factory, thread
):
    solution = thread_reply_factory(thread, poster="OtherUser")
    select_thread_solution(thread, solution, "Moderator")

    message = solution_post_status_message(solution)

    assert message == {
        "id": "solution",
        "template_name": "misago/post_status_messages/solution.html",
        "selected_at": thread.solution_selected_at,
        "selected_by": None,
        "selected_by_name": "Moderator",
        "is_locked": False,
        "locked_at": None,
        "locked_by": None,
        "locked_by_name": None,
        "lock_url": None,
        "unlock_url": None,
        "clear_url": None,
    }


def test_solution_post_status_message_returns_message_for_solution_in_thread_locked_by_user(
    thread_reply_factory, user, thread
):
    solution = thread_reply_factory(thread, poster="OtherUser")
    select_thread_solution(thread, solution, "Moderator")
    lock_thread_solution(thread, user)

    message = solution_post_status_message(solution)

    assert message == {
        "id": "solution",
        "template_name": "misago/post_status_messages/solution.html",
        "selected_at": thread.solution_selected_at,
        "selected_by": None,
        "selected_by_name": "Moderator",
        "is_locked": True,
        "locked_at": thread.solution_locked_at,
        "locked_by": {
            "id": user.id,
            "username": user.username,
            "slug": user.slug,
        },
        "locked_by_name": user.username,
        "lock_url": None,
        "unlock_url": None,
        "clear_url": None,
    }


def test_solution_post_status_message_returns_message_for_solution_in_thread_locked_by_deleted_user(
    thread_reply_factory, thread
):
    solution = thread_reply_factory(thread, poster="OtherUser")
    select_thread_solution(thread, solution, "Moderator")
    lock_thread_solution(thread, "OldModerator")

    message = solution_post_status_message(solution)

    assert message == {
        "id": "solution",
        "template_name": "misago/post_status_messages/solution.html",
        "selected_at": thread.solution_selected_at,
        "selected_by": None,
        "selected_by_name": "Moderator",
        "is_locked": True,
        "locked_at": thread.solution_locked_at,
        "locked_by": None,
        "locked_by_name": "OldModerator",
        "lock_url": None,
        "unlock_url": None,
        "clear_url": None,
    }


def test_solution_post_status_message_returns_message_for_solution_in_thread_with_extra_data(
    thread_reply_factory, thread
):
    solution = thread_reply_factory(thread, poster="OtherUser")
    select_thread_solution(thread, solution, "Moderator")

    message = solution_post_status_message(
        solution, {"lock_url": "/url/", "extra": True}
    )

    assert message == {
        "id": "solution",
        "template_name": "misago/post_status_messages/solution.html",
        "selected_at": thread.solution_selected_at,
        "selected_by": None,
        "selected_by_name": "Moderator",
        "is_locked": False,
        "locked_at": None,
        "locked_by": None,
        "locked_by_name": None,
        "lock_url": "/url/",
        "unlock_url": None,
        "clear_url": None,
        "extra": True,
    }
