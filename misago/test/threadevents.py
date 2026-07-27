import pytest
from django.utils import timezone

from ..threadevents.enums import ThreadEventTypeName
from ..threadevents.models import ThreadEvent


@pytest.fixture
def thread_event(user, thread):
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.UNLOCKED,
    )


@pytest.fixture
def thread_event_context(user, thread):
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.MERGED,
        context="Other thread",
    )


@pytest.fixture
def thread_event_category_context(user, thread, sibling_category):
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.MOVED,
        context=sibling_category.name,
        context_type="misago_categories.category",
        context_id=sibling_category.id,
    )


@pytest.fixture
def thread_event_thread_context(user, thread, other_thread):
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.SPLIT_POSTS_FROM,
        context=other_thread.title,
        context_type="misago_threads.thread",
        context_id=other_thread.id,
    )


@pytest.fixture
def thread_event_user_context(user, thread, other_user):
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.LEFT,
        context=other_user.username,
        context_type="misago_users.user",
        context_id=other_user.id,
    )


@pytest.fixture
def hidden_thread_event(user, moderator, thread):
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.UNLOCKED,
        is_hidden=True,
        hidden_by=moderator,
        hidden_by_name=moderator.username,
        hidden_at=timezone.now(),
    )


@pytest.fixture
def private_thread_event(user, private_thread):
    return ThreadEvent.objects.create(
        category=private_thread.category,
        thread=private_thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.JOINED,
    )


@pytest.fixture
def user_private_thread_event(user, user_private_thread):
    return ThreadEvent.objects.create(
        category=user_private_thread.category,
        thread=user_private_thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.JOINED,
    )


@pytest.fixture
def hidden_private_thread_event(user, moderator, private_thread):
    return ThreadEvent.objects.create(
        category=private_thread.category,
        thread=private_thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.JOINED,
        is_hidden=True,
        hidden_by=moderator,
        hidden_by_name=moderator.username,
        hidden_at=timezone.now(),
    )


@pytest.fixture
def hidden_user_private_thread_event(user, moderator, user_private_thread):
    return ThreadEvent.objects.create(
        category=user_private_thread.category,
        thread=user_private_thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.JOINED,
        is_hidden=True,
        hidden_by=moderator,
        hidden_by_name=moderator.username,
        hidden_at=timezone.now(),
    )
