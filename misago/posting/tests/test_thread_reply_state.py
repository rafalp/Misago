from ...parser.parse import parse
from ..state import ThreadReplyState


def test_thread_reply_state_save(user_request, other_user_thread):
    state = ThreadReplyState(user_request, other_user_thread)
    state.set_post_message(parse("Test reply"))
    state.save()


def test_thread_reply_state_saves_unapproved_post(
    user_request, user, default_category, other_user_thread
):
    user.require_content_approval = True
    user.save()

    state = ThreadReplyState(user_request, other_user_thread)
    state.set_post_message(parse("Test reply"))
    state.save()

    default_category.refresh_from_db()
    assert default_category.threads == 1
    assert default_category.posts == 1
    assert default_category.unapproved_threads == 0
    assert default_category.unapproved_posts == 1
    assert default_category.last_thread == other_user_thread
    assert default_category.last_posted_at == other_user_thread.started_at
    assert default_category.last_poster == other_user_thread.last_poster
    assert default_category.last_poster_name == other_user_thread.last_poster_name
    assert default_category.last_poster_slug == other_user_thread.last_poster_slug

    other_user_thread.refresh_from_db()
    assert other_user_thread.replies == 0
    assert other_user_thread.has_unapproved_posts
    assert other_user_thread.last_poster == other_user_thread.starter
    assert other_user_thread.last_poster_name == other_user_thread.starter_name
    assert other_user_thread.last_poster_slug == other_user_thread.starter_slug
    assert other_user_thread.last_posted_at == other_user_thread.started_at

    assert state.post.is_unapproved
