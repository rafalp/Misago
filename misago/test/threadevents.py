import pytest
from django.contrib.contenttypes.models import ContentType
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
def thread_event_detail(user, thread):
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.MERGED,
        detail="Other thread",
    )


@pytest.fixture
def thread_event_category_content(user, thread, sibling_category):
    content_type = ContentType.objects.get_for_model(sibling_category)
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.MOVED,
        detail=sibling_category.name,
        content_type=content_type,
        object_id=sibling_category.id,
    )


@pytest.fixture
def thread_event_thread_content(user, thread, other_thread):
    content_type = ContentType.objects.get_for_model(other_thread)
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.SPLIT_POSTS_FROM,
        detail=other_thread.title,
        content_type=content_type,
        object_id=other_thread.id,
    )


@pytest.fixture
def thread_event_user_content(user, thread, other_user):
    content_type = ContentType.objects.get_for_model(other_user)
    return ThreadEvent.objects.create(
        category=thread.category,
        thread=thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.MEMBER_LEFT,
        detail=other_user.username,
        content_type=content_type,
        object_id=other_user.id,
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
        event_type=ThreadEventTypeName.MEMBER_JOINED,
    )


@pytest.fixture
def user_private_thread_event(user, user_private_thread):
    return ThreadEvent.objects.create(
        category=user_private_thread.category,
        thread=user_private_thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.MEMBER_JOINED,
    )


@pytest.fixture
def hidden_private_thread_event(user, moderator, private_thread):
    return ThreadEvent.objects.create(
        category=private_thread.category,
        thread=private_thread,
        actor=user,
        actor_name=user.username,
        event_type=ThreadEventTypeName.MEMBER_JOINED,
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
        event_type=ThreadEventTypeName.MEMBER_JOINED,
        is_hidden=True,
        hidden_by=moderator,
        hidden_by_name=moderator.username,
        hidden_at=timezone.now(),
    )
