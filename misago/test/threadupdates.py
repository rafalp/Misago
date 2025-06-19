import pytest
from django.utils import timezone

from ..threadupdates.enums import ThreadUpdateActionName
from ..threadupdates.models import ThreadUpdate


@pytest.fixture
def thread_update(user, thread):
    return ThreadUpdate.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.OPENED,
    )


@pytest.fixture
def thread_update_context(user, thread):
    return ThreadUpdate.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.MERGED,
        context="Other thread",
    )


@pytest.fixture
def thread_update_category_context(user, thread, sibling_category):
    return ThreadUpdate.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.MOVED,
        context=sibling_category.name,
        context_type="misago_categories.category",
        context_id=sibling_category.id,
    )


@pytest.fixture
def thread_update_thread_context(user, thread, other_thread):
    return ThreadUpdate.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.SPLIT,
        context=other_thread.title,
        context_type="misago_threads.thread",
        context_id=other_thread.id,
    )


@pytest.fixture
def thread_update_user_context(user, thread, other_user):
    return ThreadUpdate.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.LEFT,
        context=other_user.username,
        context_type="misago_users.user",
        context_id=other_user.id,
    )


@pytest.fixture
def hidden_thread_update(user, moderator, thread):
    return ThreadUpdate.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.OPENED,
        is_hidden=True,
        hidden_by=moderator,
        hidden_by_name=moderator.username,
        hidden_at=timezone.now(),
    )


@pytest.fixture
def private_thread_update(user, private_thread):
    return ThreadUpdate.objects.create(
        category=private_thread.category,
        thread=private_thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.JOINED,
    )


@pytest.fixture
def user_private_thread_update(user, user_private_thread):
    return ThreadUpdate.objects.create(
        category=user_private_thread.category,
        thread=user_private_thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.JOINED,
    )


@pytest.fixture
def hidden_private_thread_update(user, moderator, private_thread):
    return ThreadUpdate.objects.create(
        category=private_thread.category,
        thread=private_thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.JOINED,
        is_hidden=True,
        hidden_by=moderator,
        hidden_by_name=moderator.username,
        hidden_at=timezone.now(),
    )


@pytest.fixture
def hidden_user_private_thread_update(user, moderator, user_private_thread):
    return ThreadUpdate.objects.create(
        category=user_private_thread.category,
        thread=user_private_thread,
        actor=user,
        actor_name=user.username,
        action=ThreadUpdateActionName.JOINED,
        is_hidden=True,
        hidden_by=moderator,
        hidden_by_name=moderator.username,
        hidden_at=timezone.now(),
    )
