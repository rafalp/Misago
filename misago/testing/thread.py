import pytest
import pytest_asyncio

from ..threads.models import Post, Thread
from ..users.models import User


@pytest.fixture
def thread_factory(category):
    default_category = category

    async def thread_test_factory(
        *,
        category=None,
        title="Thread",
        starter="Guest",
        is_closed=False,
    ):
        if isinstance(starter, User):
            starter_data = {"starter": starter}
            poster_data = {"poster": starter}
        else:
            starter_data = {"starter_name": str(starter)}
            poster_data = {"poster_name": str(starter)}

        thread = await Thread.create(
            category or default_category,
            title,
            is_closed=is_closed,
            **starter_data,
        )
        post = await Post.create(thread, **poster_data)
        thread = await thread.update(first_post=post, last_post=post)
        return thread, post

    return thread_test_factory


@pytest_asyncio.fixture
async def thread_and_post(thread_factory):
    return await thread_factory()


@pytest.fixture
def thread(thread_and_post):
    thread, _ = thread_and_post
    return thread


@pytest.fixture
def post(thread_and_post):
    _, post = thread_and_post
    return post


@pytest_asyncio.fixture
async def reply(thread):
    reply = await Post.create(thread, poster_name="Guest")
    await thread.update(replies=1, last_post=reply)
    return reply


@pytest_asyncio.fixture
async def thread_and_reply(thread):
    reply = await Post.create(thread, poster_name="Guest")
    thread = await thread.update(replies=1, last_post=reply)
    return thread, reply


@pytest_asyncio.fixture
async def thread_with_reply(thread_and_reply):
    thread, _ = thread_and_reply
    return thread


@pytest_asyncio.fixture
async def thread_reply(thread_and_reply):
    _, reply = thread_and_reply
    return reply


@pytest_asyncio.fixture
async def user_thread_and_post(thread_factory, user):
    return await thread_factory(starter=user)


@pytest.fixture
def user_thread(user_thread_and_post):
    thread, _ = user_thread_and_post
    return thread


@pytest.fixture
def user_post(user_thread_and_post):
    _, post = user_thread_and_post
    return post


@pytest_asyncio.fixture
async def other_user_thread_and_post(thread_factory, other_user):
    return await thread_factory(starter=other_user)


@pytest.fixture
def other_user_thread(other_user_thread_and_post):
    thread, _ = other_user_thread_and_post
    return thread


@pytest.fixture
def other_user_post(other_user_thread_and_post):
    _, post = other_user_thread_and_post
    return post


@pytest_asyncio.fixture
async def closed_thread_and_post(thread_factory):
    return await thread_factory(is_closed=True)


@pytest.fixture
def closed_thread(closed_thread_and_post):
    thread, _ = closed_thread_and_post
    return thread


@pytest.fixture
def closed_thread_post(closed_thread_and_post):
    _, post = closed_thread_and_post
    return post


@pytest_asyncio.fixture
async def closed_category_thread_and_post(closed_category, thread_factory):
    return await thread_factory(category=closed_category)


@pytest.fixture
def closed_category_thread(closed_category_thread_and_post):
    thread, _ = closed_category_thread_and_post
    return thread


@pytest.fixture
def closed_category_post(closed_category_thread_and_post):
    _, post = closed_category_thread_and_post
    return post


@pytest_asyncio.fixture
async def closed_user_thread_and_post(thread_factory, user):
    return await thread_factory(is_closed=True, starter=user)


@pytest.fixture
def closed_user_thread(closed_user_thread_and_post):
    thread, _ = closed_user_thread_and_post
    return thread


@pytest.fixture
def closed_user_thread_post(closed_user_thread_and_post):
    _, post = closed_user_thread_and_post
    return post


@pytest_asyncio.fixture
async def closed_category_user_thread_and_post(closed_category, thread_factory, user):
    return await thread_factory(category=closed_category, starter=user)


@pytest.fixture
def closed_category_user_thread(closed_category_user_thread_and_post):
    thread, _ = closed_category_user_thread_and_post
    return thread


@pytest.fixture
def closed_category_user_post(closed_category_user_thread_and_post):
    _, post = closed_category_user_thread_and_post
    return post
