import pytest

from ...categories.synchronize import synchronize_category
from ...likes.like import like_post
from ...notifications.threads import watch_thread
from ...notifications.users import notify_user
from ...polls.models import Poll, PollVote
from ...postedits.create import create_post_edit
from ...readtracker.models import ReadThread
from ...readtracker.tracker import mark_thread_read
from ...solutions.select import select_thread_solution
from ...threadupdates.create import create_test_thread_update
from ..create import create_thread
from ..merge import (
    get_thread_merge_conflicts,
    get_thread_merge_form_fields,
    merge_threads,
)
from ..models import Thread


def test_get_thread_merge_conflicts_returns_no_conflicts(thread, user_thread):
    conflicts = get_thread_merge_conflicts([thread, user_thread])
    assert not conflicts


def test_get_thread_merge_conflicts_returns_poll_conflict(
    poll_factory, thread, user_thread, other_user_thread
):
    thread_poll = poll_factory(thread)
    user_thread_poll = poll_factory(user_thread)

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {
        "poll": sorted([thread_poll, user_thread_poll], key=lambda i: i.thread_id),
    }


def test_get_thread_merge_conflicts_returns_single_poll(
    poll_factory, thread, user_thread, other_user_thread
):
    user_thread_poll = poll_factory(user_thread)

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {"poll": [user_thread_poll]}


def test_get_thread_merge_conflicts_returns_solution_conflict(
    thread_reply_factory, thread, user_thread, other_user_thread
):
    thread_solution = thread_reply_factory(thread, poster="DeletedUser")
    user_thread_solution = thread_reply_factory(user_thread, poster="DeletedUser")

    select_thread_solution(thread, thread_solution, "John")
    select_thread_solution(user_thread, user_thread_solution, "Bob")

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {
        "solution": sorted([thread, user_thread], key=lambda i: i.id),
    }


def test_get_thread_merge_conflicts_returns_single_solution(
    thread_reply_factory, thread, user_thread, other_user_thread
):
    user_thread_solution = thread_reply_factory(user_thread, poster="DeletedUser")
    select_thread_solution(user_thread, user_thread_solution, "Bob")

    conflicts = get_thread_merge_conflicts([thread, user_thread, other_user_thread])
    assert conflicts == {
        "solution": [user_thread],
    }


def test_get_thread_merge_form_fields_returns_poll_select_for_multiple_polls(
    poll_factory, thread, user_thread
):
    thread_poll = poll_factory(thread)
    user_thread_poll = poll_factory(user_thread)

    fields = get_thread_merge_form_fields({"poll": [thread_poll, user_thread_poll]})
    assert fields["poll"]


def test_get_thread_merge_form_fields_doesnt_return_poll_select_for_single_poll(
    poll_factory, thread
):
    thread_poll = poll_factory(thread)

    fields = get_thread_merge_form_fields({"poll": [thread_poll]})
    assert "poll" not in fields


def test_get_thread_merge_form_fields_returns_solution_select_for_multiple_solutions(
    thread_reply_factory, thread, user_thread
):
    thread_solution = thread_reply_factory(thread, poster="DeletedUser")
    user_thread_solution = thread_reply_factory(user_thread, poster="DeletedUser")

    select_thread_solution(thread, thread_solution, "John")
    select_thread_solution(user_thread, user_thread_solution, "Bob")

    fields = get_thread_merge_form_fields({"solution": [thread, user_thread]})
    assert fields["solution"]


def test_get_thread_merge_form_fields_doesnt_return_solution_select_for_single_solution(
    thread_reply_factory, thread
):
    thread_solution = thread_reply_factory(thread, poster="DeletedUser")
    select_thread_solution(thread, thread_solution, "John")

    fields = get_thread_merge_form_fields({"solution": [thread]})
    assert "solution" not in fields


def test_merge_threads_merges_threads_posts(
    sibling_category, thread, user_thread, other_user_thread
):
    thread_post = thread.first_post
    user_thread_post = user_thread.first_post
    other_user_thread_post = other_user_thread.first_post

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    thread_post.refresh_from_db()
    assert thread_post.category == sibling_category
    assert thread_post.thread == new_thread

    user_thread_post.refresh_from_db()
    assert user_thread_post.category == sibling_category
    assert user_thread_post.thread == new_thread

    other_user_thread_post.refresh_from_db()
    assert other_user_thread_post.category == sibling_category
    assert other_user_thread_post.thread == new_thread


def test_merge_threads_merges_threads_solutions(
    thread_reply_factory, sibling_category, thread, user_thread, other_user_thread
):
    thread_solution = thread_reply_factory(thread, poster="PosterA")
    user_thread_solution = thread_reply_factory(thread, poster="PosterB")
    other_user_thread_solution = thread_reply_factory(thread, poster="PosterD")

    select_thread_solution(thread, thread_solution, "John")
    select_thread_solution(user_thread, user_thread_solution, "Bob")
    select_thread_solution(other_user_thread, other_user_thread_solution, "Alice")

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(
        new_thread,
        [thread, user_thread, other_user_thread],
        {"solution": user_thread},
    )

    new_thread.refresh_from_db()
    assert new_thread.solution == user_thread_solution


def test_merge_threads_keeps_new_thread_solution(
    thread_reply_factory, sibling_category, thread, user_thread, other_user_thread
):
    thread_solution = thread_reply_factory(thread, poster="PosterA")
    user_thread_solution = thread_reply_factory(thread, poster="PosterB")
    other_user_thread_solution = thread_reply_factory(thread, poster="PosterD")

    select_thread_solution(thread, thread_solution, "John")
    select_thread_solution(user_thread, user_thread_solution, "Bob")
    select_thread_solution(other_user_thread, other_user_thread_solution, "Alice")

    new_thread = create_thread(sibling_category, "Merged thread")

    new_thread_solution = thread_reply_factory(new_thread, poster="PosterA")
    select_thread_solution(new_thread, new_thread_solution, "Diana")

    merge_threads(
        new_thread,
        [thread, user_thread, other_user_thread],
        {"solution": new_thread},
    )

    new_thread.refresh_from_db()
    assert new_thread.solution == new_thread_solution


def test_merge_threads_merges_attachments(
    sibling_category, thread, user_thread, other_user_thread, text_attachment
):
    text_attachment.associate_with_post(thread.first_post)
    text_attachment.save()

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    text_attachment.refresh_from_db()
    assert text_attachment.category == sibling_category
    assert text_attachment.thread == new_thread


def test_merge_threads_merges_poll_with_votes(
    poll_factory,
    poll_vote_factory,
    sibling_category,
    thread,
    user_thread,
    other_user_thread,
):
    thread_poll = poll_factory(thread)
    thread_poll_vote = poll_vote_factory(thread_poll, "OtherUser", "choice2")

    user_thread_poll = poll_factory(user_thread)
    user_thread_poll_vote = poll_vote_factory(user_thread_poll, "OtherUser", "choice2")

    other_user_thread_poll = poll_factory(other_user_thread)
    other_user_thread_poll_vote = poll_vote_factory(
        other_user_thread_poll, "OtherUser", "choice2"
    )

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(
        new_thread,
        [thread, user_thread, other_user_thread],
        {"poll": user_thread_poll},
    )

    user_thread_poll.refresh_from_db()
    assert user_thread_poll.category == sibling_category
    assert user_thread_poll.thread == new_thread

    user_thread_poll_vote.refresh_from_db()
    assert user_thread_poll_vote.category == sibling_category
    assert user_thread_poll_vote.thread == new_thread

    with pytest.raises(Poll.DoesNotExist):
        thread_poll.refresh_from_db()

    with pytest.raises(PollVote.DoesNotExist):
        thread_poll_vote.refresh_from_db()

    with pytest.raises(Poll.DoesNotExist):
        other_user_thread_poll.refresh_from_db()

    with pytest.raises(PollVote.DoesNotExist):
        other_user_thread_poll_vote.refresh_from_db()


def test_merge_threads_merges_likes(
    sibling_category, thread, user_thread, other_user_thread
):
    thread_like = like_post(thread.first_post, "Bob")
    user_thread_like = like_post(user_thread.first_post, "Alice")
    other_user_thread_like = like_post(other_user_thread.first_post, "Jogn")

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    thread_like.refresh_from_db()
    assert thread_like.category == sibling_category
    assert thread_like.thread == new_thread

    user_thread_like.refresh_from_db()
    assert user_thread_like.category == sibling_category
    assert user_thread_like.thread == new_thread

    other_user_thread_like.refresh_from_db()
    assert other_user_thread_like.category == sibling_category
    assert other_user_thread_like.thread == new_thread


def test_merge_threads_merges_post_edits(
    sibling_category, thread, user_thread, other_user_thread
):
    thread_post_edit = create_post_edit(
        post=thread.first_post,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )
    user_thread_post_edit = create_post_edit(
        post=user_thread.first_post,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )
    other_user_thread_post_edit = create_post_edit(
        post=other_user_thread.first_post,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    thread_post_edit.refresh_from_db()
    assert thread_post_edit.category == sibling_category
    assert thread_post_edit.thread == new_thread

    user_thread_post_edit.refresh_from_db()
    assert user_thread_post_edit.category == sibling_category
    assert user_thread_post_edit.thread == new_thread

    other_user_thread_post_edit.refresh_from_db()
    assert other_user_thread_post_edit.category == sibling_category
    assert other_user_thread_post_edit.thread == new_thread


def test_merge_threads_merges_thread_notifications(
    user, sibling_category, thread, user_thread, other_user_thread
):
    thread_notification = notify_user(
        user, "TEST", "DeletedUser", thread.category, thread
    )
    user_thread_notification = notify_user(
        user, "TEST", "DeletedUser", user_thread.category, user_thread
    )
    other_user_thread_notification = notify_user(
        user, "TEST", "DeletedUser", other_user_thread.category, other_user_thread
    )

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    thread_notification.refresh_from_db()
    assert thread_notification.category == sibling_category
    assert thread_notification.thread == new_thread

    user_thread_notification.refresh_from_db()
    assert user_thread_notification.category == sibling_category
    assert user_thread_notification.thread == new_thread

    other_user_thread_notification.refresh_from_db()
    assert other_user_thread_notification.category == sibling_category
    assert other_user_thread_notification.thread == new_thread


def test_merge_threads_merges_watched_threads(
    user, sibling_category, thread, user_thread, other_user_thread
):
    watched_thread = watch_thread(thread, user)
    watched_user_thread = watch_thread(user_thread, user)
    watched_other_user_thread = watch_thread(other_user_thread, user)

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    watched_thread.refresh_from_db()
    assert watched_thread.category == sibling_category
    assert watched_thread.thread == new_thread

    watched_user_thread.refresh_from_db()
    assert watched_user_thread.category == sibling_category
    assert watched_user_thread.thread == new_thread

    watched_other_user_thread.refresh_from_db()
    assert watched_other_user_thread.category == sibling_category
    assert watched_other_user_thread.thread == new_thread


def test_merge_threads_merges_thread_post_notifications(
    user, sibling_category, thread, user_thread, other_user_thread
):
    thread_notification = notify_user(
        user,
        "TEST",
        "DeletedUser",
        thread.category,
        thread,
        thread.first_post,
    )
    user_thread_notification = notify_user(
        user,
        "TEST",
        "DeletedUser",
        user_thread.category,
        user_thread,
        user_thread.first_post,
    )
    other_user_thread_notification = notify_user(
        user,
        "TEST",
        "DeletedUser",
        other_user_thread.category,
        other_user_thread,
        other_user_thread.first_post,
    )

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    thread_notification.refresh_from_db()
    assert thread_notification.category == sibling_category
    assert thread_notification.thread == new_thread

    user_thread_notification.refresh_from_db()
    assert user_thread_notification.category == sibling_category
    assert user_thread_notification.thread == new_thread

    other_user_thread_notification.refresh_from_db()
    assert other_user_thread_notification.category == sibling_category
    assert other_user_thread_notification.thread == new_thread


def test_merge_threads_deletes_thread_reads(
    user, sibling_category, thread, user_thread, other_user_thread
):
    mark_thread_read(user, thread, thread.last_posted_at)
    mark_thread_read(user, user_thread, user_thread.last_posted_at)
    mark_thread_read(user, other_user_thread, other_user_thread.last_posted_at)

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    assert not ReadThread.objects.exists()


def test_merge_threads_merges_thread_updates(
    sibling_category, thread, user_thread, other_user_thread
):
    thread_update = create_test_thread_update(thread, "DeletedUser")
    user_thread_update = create_test_thread_update(user_thread, "DeletedUser")
    other_user_thread_update = create_test_thread_update(
        other_user_thread, "DeletedUser"
    )

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    thread_update.refresh_from_db()
    assert thread_update.category == sibling_category
    assert thread_update.thread == new_thread

    user_thread_update.refresh_from_db()
    assert user_thread_update.category == sibling_category
    assert user_thread_update.thread == new_thread

    other_user_thread_update.refresh_from_db()
    assert other_user_thread_update.category == sibling_category
    assert other_user_thread_update.thread == new_thread


def test_merge_threads_deletes_old_threads(
    default_category, sibling_category, thread, user_thread, other_user_thread
):
    synchronize_category(default_category)

    thread.category = default_category
    user_thread.category = default_category
    other_user_thread.category = default_category

    assert default_category.last_thread

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(new_thread, [thread, user_thread, other_user_thread], {})

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        user_thread.refresh_from_db()

    with pytest.raises(Thread.DoesNotExist):
        other_user_thread.refresh_from_db()

    assert default_category.last_thread is None


def test_merge_threads_save_target_if_commit_is_false(
    thread_reply_factory, sibling_category, thread, user_thread, other_user_thread
):
    user_thread_solution = thread_reply_factory(thread, poster="PosterB")
    select_thread_solution(user_thread, user_thread_solution, "Bob")

    new_thread = create_thread(sibling_category, "Merged thread")
    merge_threads(
        new_thread,
        [thread, user_thread, other_user_thread],
        {"solution": user_thread},
        commit=False,
    )

    assert new_thread.solution == user_thread_solution

    new_thread.refresh_from_db()
    assert new_thread.solution is None
