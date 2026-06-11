import pytest

from ...likes.like import like_post
from ...likes.models import Like
from ...notifications.models import Notification, WatchedThread
from ...notifications.threads import watch_thread
from ...notifications.users import notify_user
from ...polls.models import Poll, PollVote
from ...postedits.create import create_post_edit
from ...postedits.models import PostEdit
from ...readtracker.models import ReadThread
from ...readtracker.tracker import mark_thread_read
from ...solutions.thread import select_thread_solution
from ..delete import delete_thread
from ..models import Post, Thread


def test_delete_thread_deletes_thread(thread, post):
    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        post.refresh_from_db()


def test_delete_thread_deletes_thread_with_reply(thread, post, reply):
    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        post.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()


def test_delete_thread_deletes_thread_with_solution(thread, post, reply):
    select_thread_solution(thread, reply, "DeletedUser")
    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        post.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()


def test_delete_thread_deletes_category_last_thread(
    default_category, thread, post, reply
):
    default_category.last_thread = thread
    default_category.save()

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        post.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    default_category.refresh_from_db()
    assert default_category.last_thread is None


def test_delete_thread_deletes_thread_poll_with_votes(
    poll_factory, poll_vote_factory, thread, reply
):
    poll = poll_factory(thread)
    poll_vote = poll_vote_factory(poll, "OtherUser", "choice2")

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(Poll.DoesNotExist):
        poll.refresh_from_db()

    with pytest.raises(PollVote.DoesNotExist):
        poll_vote.refresh_from_db()


def test_delete_thread_deletes_thread_post_like(thread, reply):
    post_like = like_post(reply, "DeletedUser")

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(Like.DoesNotExist):
        post_like.refresh_from_db()


def test_delete_thread_deletes_thread_post_edit(thread, reply):
    post_edit = create_post_edit(
        post=reply,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_delete_thread_deletes_thread_notification(user, thread, reply):
    notification = notify_user(user, "TEST", "DeletedUser", thread.category, thread)

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_delete_thread_deletes_thread_post_notification(user, thread, reply):
    notification = notify_user(
        user, "TEST", "DeletedUser", thread.category, thread, reply
    )

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_delete_thread_deletes_read_thread(user, thread, reply):
    read_thread = mark_thread_read(user, thread, reply.posted_at)

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    assert not ReadThread.objects.exists()


def test_delete_thread_deletes_thread_watch(user, thread, reply):
    watched_thread = watch_thread(thread, user)

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(WatchedThread.DoesNotExist):
        watched_thread.refresh_from_db()


def test_delete_thread_marks_attachments_for_deletion(thread, reply, text_attachment):
    text_attachment.associate_with_post(reply)
    text_attachment.save()

    delete_thread(thread)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    text_attachment.refresh_from_db()
    assert text_attachment.category is None
    assert text_attachment.thread is None
    assert text_attachment.post is None
    assert text_attachment.is_deleted
