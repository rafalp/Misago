from unittest.mock import Mock

import pytest

from ...notifications.models import Notification
from ..cursor import PaginationError, paginate_queryset


def test_pagination_raises_error_if_after_is_not_a_number():
    request = Mock(GET={"after": "str"})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, "id", 100)

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_before_is_not_a_number():
    request = Mock(GET={"before": "str"})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, "id", 100)

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_after_is_zero():
    request = Mock(GET={"after": 0})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, "id", 100)

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_before_is_zero():
    request = Mock(GET={"before": 0})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, "id", 100)

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_after_is_negative():
    request = Mock(GET={"after": -1})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, "id", 100)

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_before_is_negative():
    request = Mock(GET={"before": -1})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, "id", 100)

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_after_and_before_are_both_set():
    request = Mock(GET={"after": 1, "before": 5})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, "id", 100)

    assert "'after' and 'before' can't be used at same time" in str(excinfo)
