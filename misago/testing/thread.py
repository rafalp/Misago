import pytest

from ..threads.models import Post, Thread


@pytest.fixture
async def thread_and_post(category):
    thread = await Thread.create(category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def thread(thread_and_post):
    thread, _ = thread_and_post
    return thread


@pytest.fixture
def post(thread_and_post):
    _, post = thread_and_post
    return post


@pytest.fixture
async def reply(thread):
    reply = await Post.create(thread, poster_name="Guest")
    await thread.update(replies=1, last_post=reply)
    return reply


@pytest.fixture
async def thread_and_reply(thread):
    reply = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(replies=1, last_post=reply)
    return thread, reply


@pytest.fixture
async def thread_with_reply(thread_and_reply):
    thread, _ = thread_and_reply
    return thread


@pytest.fixture
async def thread_reply(thread_and_reply):
    _, reply = thread_and_reply
    return reply


@pytest.fixture
async def user_thread_and_post(category, user):
    thread = await Thread.create(category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster=user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def user_thread(user_thread_and_post):
    thread, _ = user_thread_and_post
    return thread


@pytest.fixture
def user_post(user_thread_and_post):
    _, post = user_thread_and_post
    return post


@pytest.fixture
async def other_user_thread_and_post(category, other_user):
    thread = await Thread.create(category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster=other_user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def other_user_thread(other_user_thread_and_post):
    thread, _ = other_user_thread_and_post
    return thread


@pytest.fixture
def other_user_post(other_user_thread_and_post):
    _, post = other_user_thread_and_post
    return post


@pytest.fixture
async def closed_thread_and_post(category):
    thread = await Thread.create(
        category, "Thread", starter_name="Guest", is_closed=True
    )
    post = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_thread(closed_thread_and_post):
    thread, _ = closed_thread_and_post
    return thread


@pytest.fixture
def closed_thread_post(closed_thread_and_post):
    _, post = closed_thread_and_post
    return post


@pytest.fixture
async def closed_category_thread_and_post(closed_category):
    thread = await Thread.create(
        closed_category,
        "Closed Category Thread",
        starter_name="Guest",
    )
    post = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_category_thread(closed_category_thread_and_post):
    thread, _ = closed_category_thread_and_post
    return thread


@pytest.fixture
def closed_category_post(closed_category_thread_and_post):
    _, post = closed_category_thread_and_post
    return post


@pytest.fixture
async def closed_user_thread_and_post(category, user):
    thread = await Thread.create(
        category, "Thread", starter_name="Guest", is_closed=True
    )
    post = await Post.create(thread, poster=user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_user_thread(closed_user_thread_and_post):
    thread, _ = closed_user_thread_and_post
    return thread


@pytest.fixture
def closed_user_thread_post(closed_user_thread_and_post):
    _, post = closed_user_thread_and_post
    return post


@pytest.fixture
async def closed_category_user_thread_and_post(closed_category, user):
    thread = await Thread.create(closed_category, "Thread", starter_name="Guest")
    post = await Post.create(thread, poster=user)
    thread = await thread.update(first_post=post, last_post=post)
    return thread, post


@pytest.fixture
def closed_category_user_thread(closed_category_user_thread_and_post):
    thread, _ = closed_category_user_thread_and_post
    return thread


@pytest.fixture
def closed_category_user_post(closed_category_user_thread_and_post):
    _, post = closed_category_user_thread_and_post
    return post
