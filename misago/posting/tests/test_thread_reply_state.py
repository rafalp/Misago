from ...parser.parse import parse
from ..state import ThreadReplyState


def test_thread_reply_state_save(user_request, other_user_thread):
    state = ThreadReplyState(user_request, other_user_thread)
    state.set_post_message(parse("Test reply"))
    state.save()
