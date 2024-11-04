from ...threads.models import ThreadParticipant
from ..state import StartPrivateThreadState


def test_start_private_thread_state_save_sets_request_user_as_thread_owner(
    user_request, private_threads_category, user, other_user
):
    state = StartPrivateThreadState(user_request, private_threads_category)
    state.set_thread_title("Test thread")
    state.set_post_message("Hello world")
    state.set_invite_users([other_user])
    state.save()

    ThreadParticipant.objects.get(
        thread=state.thread,
        user=user,
        is_owner=True,
    )


def test_start_private_thread_state_save_invites_users_to_saved_thread(
    user_request, private_threads_category, other_user
):
    state = StartPrivateThreadState(user_request, private_threads_category)
    state.set_thread_title("Test thread")
    state.set_post_message("Hello world")
    state.set_invite_users([other_user])
    state.save()

    ThreadParticipant.objects.get(
        thread=state.thread,
        user=other_user,
        is_owner=False,
    )
