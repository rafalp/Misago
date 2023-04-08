import pytest

from ..models import WatchedThread
from ..threads import ThreadNotifications


@pytest.fixture
def watched_thread_factory():
    def create_watched_thread(
        user, thread, notifications: ThreadNotifications = ThreadNotifications.NONE
    ):
        return WatchedThread.objects.create(
            user=user,
            category_id=thread.category_id,
            thread=thread,
            notifications=notifications,
        )

    return create_watched_thread
