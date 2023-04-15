from unittest.mock import Mock

import pytest
from django.http import Http404

from ....notifications.models import Notification
from ..pagination import paginate_queryset


def test_pagination_with_after_returns_items_up_to_max_limit(notifications):
    request = Mock(GET={"after": notifications[4]})
    page = paginate_queryset(request, Notification.objects, "id", 4)

    assert len(page.items) == 4
    assert page.has_next
    assert page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_5", "test_6", "test_7", "test_8"]


def test_pagination_with_after_returns_items_up_to_given_limit(notifications):
    request = Mock(GET={"after": notifications[4], "limit": 5})
    page = paginate_queryset(request, Notification.objects, "id", 10)

    assert len(page.items) == 5
    assert page.has_next
    assert page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_5", "test_6", "test_7", "test_8", "test_9"]


def test_pagination_with_after_returns_last_items(notifications):
    request = Mock(GET={"after": notifications[9]})
    page = paginate_queryset(request, Notification.objects, "id", 10)

    assert len(page.items) == 5
    assert not page.has_next
    assert page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_10", "test_11", "test_12", "test_13", "test_14"]


def test_pagination_with_after_returns_empty_items(notifications):
    request = Mock(GET={"after": notifications[14]})
    page = paginate_queryset(request, Notification.objects, "id", 10, raise_404=False)

    assert len(page.items) == 0
    assert not page.has_next
    assert not page.has_previous


def test_pagination_with_after_raises_404_for_empty_item(notifications):
    request = Mock(GET={"after": notifications[14]})
    with pytest.raises(Http404):
        paginate_queryset(request, Notification.objects, "id", 10, raise_404=True)


def test_pagination_with_after_returns_items_up_to_max_limit_in_reverse_order(
    notifications,
):
    request = Mock(GET={"after": notifications[9]})
    page = paginate_queryset(request, Notification.objects, "-id", 4)

    assert len(page.items) == 4
    assert page.has_next
    assert page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_8", "test_7", "test_6", "test_5"]


def test_pagination_with_after_returns_items_up_to_given_limit_in_reverse_order(
    notifications,
):
    request = Mock(GET={"after": notifications[9], "limit": 5})
    page = paginate_queryset(request, Notification.objects, "-id", 10)

    assert len(page.items) == 5
    assert page.has_next
    assert page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_8", "test_7", "test_6", "test_5", "test_4"]


def test_pagination_with_after_returns_last_items_in_reverse_order(notifications):
    request = Mock(GET={"after": notifications[4]})
    page = paginate_queryset(request, Notification.objects, "-id", 10)

    assert len(page.items) == 4
    assert not page.has_next
    assert page.has_previous

    items_verbs = [item.verb for item in page.items]
    assert items_verbs == ["test_3", "test_2", "test_1", "test_0"]
