from ...parser.parse import parse
from ..state import PrivateThreadReplyState


def test_private_thread_reply_state_save(user_request, user_private_thread):
    state = PrivateThreadReplyState(user_request, user_private_thread)
    state.set_post_message(parse("Test reply"))
    state.save()


def test_private_thread_reply_state_saves_unapproved_post(
    user_request, user, other_user_private_thread
):
    user.require_content_approval = True
    user.save()

    state = PrivateThreadReplyState(user_request, other_user_private_thread)
    state.set_post_message(parse("Test reply"))
    state.save()

    other_user_private_thread.refresh_from_db()
    assert other_user_private_thread.replies == 0
    assert other_user_private_thread.has_unapproved_posts
    assert other_user_private_thread.last_poster == other_user_private_thread.starter
    assert (
        other_user_private_thread.last_poster_name
        == other_user_private_thread.starter_name
    )
    assert (
        other_user_private_thread.last_poster_slug
        == other_user_private_thread.starter_slug
    )
    assert (
        other_user_private_thread.last_posted_at == other_user_private_thread.started_at
    )

    assert state.post.is_unapproved
