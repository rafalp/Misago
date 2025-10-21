from ...parser.parse import parse
from ..state import PrivateThreadReplyState


def test_private_thread_reply_state_save(user_request, user_private_thread):
    state = PrivateThreadReplyState(user_request, user_private_thread)
    state.set_post_message(parse("Test reply"))
    state.save()
