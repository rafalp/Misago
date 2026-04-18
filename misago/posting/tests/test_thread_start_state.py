from ...parser.parse import parse
from ...polls.models import Poll
from ..state import ThreadStartState


def test_thread_start_state_creates_thread_with_poll(user_request, default_category):
    state = ThreadStartState(user_request, default_category)

    poll = Poll(
        category=state.category,
        thread=state.thread,
        starter=state.user,
        starter_name=state.user.username,
        starter_slug=state.user.slug,
        question="Test",
        choices=[],
    )

    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.set_poll(poll)
    state.save()

    assert state.thread.id
    assert state.thread.has_poll
    assert state.post.id
    assert state.post.thread == state.thread
    assert state.poll.id
    assert Poll.objects.get(thread=state.thread) == state.poll


def test_thread_start_state_saves_unapproved_thread(
    user_request, user, default_category
):
    user.require_content_approval = True
    user.save()

    state = ThreadStartState(user_request, default_category)

    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.save()

    assert state.thread.is_unapproved
    assert not state.post.is_unapproved

    default_category.refresh_from_db()
    assert default_category.threads == 0
    assert default_category.posts == 0
    assert default_category.unapproved_threads == 1
    assert default_category.unapproved_posts == 0
    assert default_category.last_thread is None
    assert default_category.last_posted_at is None
    assert default_category.last_poster is None
    assert default_category.last_poster_name is None
    assert default_category.last_poster_slug is None
