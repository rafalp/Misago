from ...parser.parse import parse
from ...polls.models import Poll
from ..state import ThreadStartState


def test_thread_start_state_creates_thread_with_poll(
    mock_upgrade_post_content, user_request, default_category
):
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
