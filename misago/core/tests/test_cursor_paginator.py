import pytest

from ..cursorpaginator import CursorPaginator, EmptyPage, InvalidPage


@pytest.fixture
def mock_objects(mocker):
    return [mocker.Mock(post=i) for i in range(1, 12)]


@pytest.fixture
def mock_queryset(mocker, mock_objects):
    return mocker.Mock(
        filter=mocker.Mock(return_value=mock_objects)
    )


def test_paginator_returns_first_page(mock_objects):
    paginator = CursorPaginator(mock_objects, "post", 6)
    assert paginator.get_page()


def test_first_page_has_no_start(mock_objects):
    paginator = CursorPaginator(mock_objects, "post", 6)
    assert paginator.get_page().start is None


def test_first_page_has_correct_length(mock_objects):
    paginator = CursorPaginator(mock_objects, "post", 6)
    assert len(paginator.get_page().object_list) == 6


def test_first_page_has_correct_items(mock_objects):
    paginator = CursorPaginator(mock_objects, "post", 6)
    assert paginator.get_page().object_list == mock_objects[:6]


def test_page_has_next_attr_pointing_to_first_item_of_next_page(mock_objects):
    paginator = CursorPaginator(mock_objects, "post", 6)
    assert paginator.get_page().next == 7


def test_page_can_be_tested_to_see_if_next_page_exists(mock_objects):
    paginator = CursorPaginator(mock_objects, "post", 6)
    assert paginator.get_page().has_next()


def test_paginator_returns_empty_first_page_without_errors():
    paginator = CursorPaginator([], "post", 6)
    assert paginator.get_page().object_list == []


def test_paginator_returns_page_starting_at_requested_address(mock_queryset):
    paginator = CursorPaginator(mock_queryset, "post", 6)
    assert paginator.get_page(7)


def test_requesting_next_page_filters_queryset_using_filter_name(mock_queryset):
    paginator = CursorPaginator(mock_queryset, "post", 6)
    paginator.get_page(7)
    mock_queryset.filter.assert_called_once_with(post__gte=7)


def test_requesting_next_page_limits_queryset_to_specified_length(mock_queryset):
    paginator = CursorPaginator(mock_queryset, "post", 6)
    assert len(paginator.get_page(7).object_list) == 6


def test_paginator_raises_empty_page_error_if_nth_page_is_empty(mocker):
    queryset = mocker.Mock(filter=lambda **_: [])
    paginator = CursorPaginator(queryset, "post", 6)
    with pytest.raises(EmptyPage):
        paginator.get_page(20)


def test_paginator_raises_invalid_page_error_if_starting_position_is_negative():
    paginator = CursorPaginator(None, None, 0)
    with pytest.raises(InvalidPage):
        paginator.get_page(-1)
