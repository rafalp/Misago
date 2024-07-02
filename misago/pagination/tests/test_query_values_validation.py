from unittest.mock import Mock

import pytest

from ...notifications.models import Notification
from ..cursor import PaginationError, paginate_queryset


def test_pagination_raises_error_if_cursor_is_not_a_number(db):
    request = Mock(GET={"cursor": "str"})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, 100, "id")

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_cursor_is_zero(db):
    request = Mock(GET={"cursor": 0})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, 100, "id")

    assert "must be a positive integer" in str(excinfo)


def test_pagination_raises_error_if_cursor_is_negative(db):
    request = Mock(GET={"cursor": -1})

    with pytest.raises(PaginationError) as excinfo:
        paginate_queryset(request, Notification.objects, 100, "id")

    assert "must be a positive integer" in str(excinfo)
