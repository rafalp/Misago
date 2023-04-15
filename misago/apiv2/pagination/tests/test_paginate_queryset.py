from unittest.mock import Mock

from ....notifications.models import Notification
from ..pagination import paginate_queryset


def test_pagination_returns_all_items(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, "id", 20)

    assert len(page.items) == 15
    assert not page.has_next
    assert not page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == [f"test_{i}" for i in range(15)]
    assert page.first_cursor == page.items[0].id
    assert page.last_cursor == page.items[-1].id


def test_pagination_returns_no_items(db):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, "id", 20)

    assert len(page.items) == 0
    assert not page.has_next
    assert not page.has_previous
    assert page.first_cursor is None
    assert page.last_cursor is None


def test_pagination_returns_firsts_and_last_cursor(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, "id", 20)

    assert len(page.items) == 15
    assert page.first_cursor == page.items[0].id
    assert page.last_cursor == page.items[-1].id


def test_pagination_returns_all_items_in_reverse_order(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, "-id", 20)

    assert len(page.items) == 15
    assert not page.has_next
    assert not page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == [f"test_{i}" for i in reversed(range(15))]


def test_pagination_returns_first_items_up_to_max_limit(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, "id", 4)

    assert len(page.items) == 4
    assert page.has_next
    assert not page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_0", "test_1", "test_2", "test_3"]


def test_pagination_returns_first_items_up_to_given_limit(notifications):
    request = Mock(GET={"limit": 5})
    page = paginate_queryset(request, Notification.objects, "id", 10)

    assert len(page.items) == 5
    assert page.has_next
    assert not page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_0", "test_1", "test_2", "test_3", "test_4"]


def test_pagination_returns_first_items_up_to_max_limit_in_reverse_order(
    notifications,
):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, "-id", 4)

    assert len(page.items) == 4
    assert page.has_next
    assert not page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_14", "test_13", "test_12", "test_11"]


def test_pagination_returns_first_items_up_to_given_limit_in_reverse_order(
    notifications,
):
    request = Mock(GET={"limit": 5})
    page = paginate_queryset(request, Notification.objects, "-id", 10)

    assert len(page.items) == 5
    assert page.has_next
    assert not page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_14", "test_13", "test_12", "test_11", "test_10"]
