from ..state import ReplyThreadState


def test_reply_thread_state_initializes_post(user_request, other_user_thread):
    state = ReplyThreadState(user_request, other_user_thread)

    assert state.thread
    assert state.thread.starter == other_user_thread.starter
    assert state.thread.starter_name == other_user_thread.starter.username
    assert state.thread.starter_slug == other_user_thread.starter.slug
    assert state.thread.last_poster == other_user_thread.last_poster
    assert state.thread.last_poster_name == other_user_thread.last_poster_name
    assert state.thread.last_poster_slug == other_user_thread.last_poster_slug
    assert state.thread.category == other_user_thread.category
    assert state.thread.started_on == other_user_thread.started_on
    assert state.thread.last_post_on == other_user_thread.last_post_on

    assert state.post
    assert state.post.poster == user_request.user
    assert state.post.poster_name == user_request.user.username
    assert state.post.category == other_user_thread.category
    assert state.post.posted_on == state.timestamp


def test_reply_thread_state_save_saves_post(user_request, other_user_thread):
    state = ReplyThreadState(user_request, other_user_thread)
    state.set_post_message("Test reply")
    state.save()

    assert state.post.id
    assert state.post.thread == state.thread


def test_reply_thread_state_updates_thread(user_request, other_user_thread):
    state = ReplyThreadState(user_request, other_user_thread)
    state.set_post_message("Test reply")
    state.save()

    other_user_thread.refresh_from_db()
    assert other_user_thread.replies == 1
    assert state.thread.last_poster == user_request.user
    assert state.thread.last_poster_name == user_request.user.username
    assert state.thread.last_poster_slug == user_request.user.slug
    assert state.thread.last_post_on == state.timestamp


def test_reply_thread_state_updates_category(user_request, other_user_thread):
    state = ReplyThreadState(user_request, other_user_thread)
    state.set_post_message("Test reply")
    state.save()

    category = other_user_thread.category

    category.refresh_from_db()
    assert category.threads == 1
    assert category.posts == 2
    assert category.last_thread == state.thread
    assert category.last_post_on == state.timestamp
    assert category.last_poster == user_request.user
    assert category.last_poster_name == user_request.user.username
    assert category.last_poster_slug == user_request.user.slug


def test_reply_thread_state_updates_user(user_request, other_user_thread, user):
    state = ReplyThreadState(user_request, other_user_thread)
    state.set_post_message("Test reply")
    state.save()

    user.refresh_from_db()
    assert user.threads == 0
    assert user.posts == 1
