from unittest.mock import Mock

from ...notifications.models import Notification
from ..cursor import paginate_queryset


def test_pagination_returns_all_items(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, 20, "id")

    assert len(page.items) == 15
    assert not page.has_next
    assert not page.has_previous
    assert page.next_cursor is None
    assert page.previous_cursor is None

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == [f"test_{i}" for i in range(15)]


def test_pagination_returns_all_items_in_reverse_order(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, 20, "-id")

    assert len(page.items) == 15
    assert not page.has_next
    assert not page.has_previous
    assert page.next_cursor is None
    assert page.previous_cursor is None

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == [f"test_{i}" for i in reversed(range(15))]


def test_pagination_returns_no_items(db):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, 20, "id")

    assert len(page.items) == 0
    assert not page.has_next
    assert not page.has_previous
    assert page.next_cursor is None
    assert page.previous_cursor is None


def test_pagination_returns_firsts_and_previous_cursor_for_first_page(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, 5, "id")

    assert len(page.items) == 5
    assert page.next_cursor == notifications[4]
    assert page.previous_cursor is None


def test_pagination_returns_firsts_and_previous_cursor_for_second_page(notifications):
    request = Mock(GET={"cursor": notifications[:5][-1]})
    page = paginate_queryset(request, Notification.objects, 5, "id")

    assert len(page.items) == 5
    assert page.next_cursor == notifications[9]
    assert page.previous_cursor is None


def test_pagination_returns_firsts_and_previous_cursor_for_last_page(notifications):
    request = Mock(GET={"cursor": notifications[:10][-1]})
    page = paginate_queryset(request, Notification.objects, 5, "id")

    assert len(page.items) == 5
    assert page.next_cursor is None
    assert page.previous_cursor == notifications[4]


def test_pagination_returns_first_items_up_to_limit(notifications):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, 4, "id")

    assert len(page.items) == 4
    assert page.has_next
    assert not page.has_previous
    assert page.next_cursor == notifications[3]
    assert page.previous_cursor is None

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_0", "test_1", "test_2", "test_3"]


def test_pagination_returns_first_items_up_to_limit_in_reverse_order(
    notifications,
):
    request = Mock(GET={})
    page = paginate_queryset(request, Notification.objects, 4, "-id")

    assert len(page.items) == 4
    assert page.has_next
    assert not page.has_previous
    assert page.next_cursor == notifications[11]
    assert page.previous_cursor is None

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_14", "test_13", "test_12", "test_11"]
