import pytest

from ....notifications.models import Notification


@pytest.fixture
def notifications(user):
    objects = Notification.objects.bulk_create(
        [Notification(user=user, verb=f"test_{i}") for i in range(15)]
    )

    return sorted([obj.id for obj in objects])
