from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..models import Poll
from ..save import save_thread_poll


def test_save_thread_poll_saves_poll_in_database(user, thread):
    poll = Poll(
        category=thread.category,
        thread=thread,
        starter=user,
        starter_name=user.username,
        starter_slug=user.slug,
        question="Question",
        choices=[],
    )

    save_thread_poll(thread, poll, user)

    assert poll.id

    poll.refresh_from_db()
    assert poll.id


def test_save_thread_poll_updates_thread_poll_flag(user, thread):
    poll = Poll(
        category=thread.category,
        thread=thread,
        starter=user,
        starter_name=user.username,
        starter_slug=user.slug,
        question="Question",
        choices=[],
    )

    save_thread_poll(thread, poll, user)

    assert thread.has_poll

    thread.refresh_from_db()
    assert thread.has_poll


def test_save_thread_poll_creates_thread_update(user, thread):
    poll = Poll(
        category=thread.category,
        thread=thread,
        starter=user,
        starter_name=user.username,
        starter_slug=user.slug,
        question="Question",
        choices=[],
    )

    save_thread_poll(thread, poll, user)

    ThreadUpdate.objects.get(thread=thread, action=ThreadUpdateActionName.STARTED_POLL)
