from ..state import StartThreadState


def test_start_thread_state_initializes_thread_and_post(user_request, default_category):
    state = StartThreadState(user_request, default_category)

    assert state.thread
    assert state.thread.starter == user_request.user
    assert state.thread.starter_name == user_request.user.username
    assert state.thread.starter_slug == user_request.user.slug
    assert state.thread.last_poster == user_request.user
    assert state.thread.last_poster_name == user_request.user.username
    assert state.thread.last_poster_slug == user_request.user.slug
    assert state.thread.category == default_category
    assert state.thread.started_on == state.timestamp
    assert state.thread.last_post_on == state.timestamp

    assert state.post
    assert state.post.poster == user_request.user
    assert state.post.poster_name == user_request.user.username
    assert state.post.category == default_category
    assert state.post.posted_on == state.timestamp


def test_start_thread_state_stores_category_state(user_request, default_category):
    state = StartThreadState(user_request, default_category)
    assert state.get_object_state(default_category)


def test_start_thread_state_set_thread_title_updates_thread_title_and_slug(
    user_request, default_category
):
    state = StartThreadState(user_request, default_category)
    state.set_thread_title("Test thread")
    assert state.thread.title == "Test thread"
    assert state.thread.slug == "test-thread"


def test_start_thread_state_save_saves_thread_and_post(user_request, default_category):
    state = StartThreadState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message("Hello world")
    state.save()

    assert state.thread.id
    assert state.post.id
    assert state.post.thread == state.thread


def test_start_thread_state_updates_category(user_request, default_category):
    state = StartThreadState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message("Hello world")
    state.save()

    default_category.refresh_from_db()
    assert default_category.threads == 1
    assert default_category.posts == 1
    assert default_category.last_thread == state.thread
    assert default_category.last_post_on == state.thread.last_post_on
    assert default_category.last_poster == state.thread.last_poster
    assert default_category.last_poster_name == state.thread.last_poster_name
    assert default_category.last_poster_slug == state.thread.last_poster_slug


def test_start_thread_state_updates_user(user_request, default_category, user):
    state = StartThreadState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message("Hello world")
    state.save()

    user.refresh_from_db()
    assert user.threads == 1
    assert user.posts == 1
