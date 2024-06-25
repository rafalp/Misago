from unittest.mock import Mock

import pytest
from django.http import Http404

from ...notifications.models import Notification
from ..cursor import paginate_queryset


def test_pagination_with_cursor_returns_items_up_to_limit(notifications):
    request = Mock(GET={"cursor": notifications[4]})
    page = paginate_queryset(request, Notification.objects, 4, "id")

    assert len(page.items) == 4
    assert page.has_next
    assert page.has_previous
    assert page.next_cursor == notifications[8]
    assert page.previous_cursor == notifications[0]

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_5", "test_6", "test_7", "test_8"]


def test_pagination_with_cursor_returns_last_items(notifications):
    request = Mock(GET={"cursor": notifications[9]})
    page = paginate_queryset(request, Notification.objects, 10, "id")

    assert len(page.items) == 5
    assert not page.has_next
    assert page.has_previous
    assert not page.next_cursor
    assert not page.previous_cursor

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_10", "test_11", "test_12", "test_13", "test_14"]


def test_pagination_with_cursor_returns_empty_items(notifications):
    request = Mock(GET={"cursor": notifications[14]})
    page = paginate_queryset(request, Notification.objects, 10, "id", raise_404=False)

    assert len(page.items) == 0
    assert not page.has_next
    assert not page.has_previous
    assert not page.next_cursor
    assert not page.previous_cursor


def test_pagination_with_cursor_raises_404_for_empty_item(notifications):
    request = Mock(GET={"cursor": notifications[14]})
    with pytest.raises(Http404):
        paginate_queryset(request, Notification.objects, 10, "id", raise_404=True)


def test_pagination_with_cursor_returns_items_up_to_limit_in_reverse_order(
    notifications,
):
    request = Mock(GET={"cursor": notifications[9]})
    page = paginate_queryset(request, Notification.objects, 4, "-id")

    assert len(page.items) == 4
    assert page.has_next
    assert page.has_previous
    assert page.next_cursor == notifications[5]
    assert page.previous_cursor == notifications[13]

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_8", "test_7", "test_6", "test_5"]


def test_pagination_with_cursor_returns_last_items_in_reverse_order(notifications):
    request = Mock(GET={"cursor": notifications[4]})
    page = paginate_queryset(request, Notification.objects, 10, "-id")

    assert len(page.items) == 4
    assert not page.has_next
    assert page.has_previous
    assert not page.next_cursor
    assert page.previous_cursor == notifications[14]

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_3", "test_2", "test_1", "test_0"]
