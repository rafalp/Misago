from ...parser.parse import parse
from ...privatethreads.models import PrivateThreadMember
from ..state import PrivateThreadStartState


def test_private_thread_start_state_save_sets_request_user_as_thread_owner(
    user_request, private_threads_category, user, other_user
):
    state = PrivateThreadStartState(user_request, private_threads_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.set_members([other_user])
    state.save()

    PrivateThreadMember.objects.get(
        thread=state.thread,
        user=user,
        is_owner=True,
    )


def test_private_thread_start_state_save_adds_members_to_saved_thread(
    user_request, private_threads_category, other_user
):
    state = PrivateThreadStartState(user_request, private_threads_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.set_members([other_user])
    state.save()

    PrivateThreadMember.objects.get(
        thread=state.thread,
        user=other_user,
        is_owner=False,
    )
