import pytest

from ..cursorpagination import CursorPage, EmptyPage, InvalidPage, get_page


@pytest.fixture
def mock_objects(mocker):
    return [mocker.Mock(post=i) for i in range(1, 12)]


@pytest.fixture
def mock_queryset(mocker, mock_objects):
    return mocker.Mock(filter=mocker.Mock(return_value=mock_objects))


def test_paginator_returns_first_page(mock_objects):
    assert get_page(mock_objects, "post", 6)


def test_first_page_has_first_flag(mock_objects):
    page = get_page(mock_objects, "post", 6)
    assert page.first


def test_first_page_start_is_zero(mock_objects):
    page = get_page(mock_objects, "post", 6)
    assert page.start == 0


def test_first_page_has_correct_length(mock_objects):
    page = get_page(mock_objects, "post", 6)
    assert len(page.object_list) == 6


def test_first_page_has_correct_items(mock_objects):
    page = get_page(mock_objects, "post", 6)
    assert page.object_list == mock_objects[:6]


def test_page_has_next_attr_pointing_to_first_item_of_next_page(mock_objects):
    page = get_page(mock_objects, "post", 6)
    assert page.next == 7


def test_requesting_next_page_filters_queryset_using_filter_name(mock_queryset):
    page = get_page(mock_queryset, "post", 6, 7)
    mock_queryset.filter.assert_called_once_with(post__gte=7)


def test_requesting_next_page_for_reversed_order_filters_queryset_with_descending(
    mock_queryset
):
    page = get_page(mock_queryset, "-post", 6, 7)
    mock_queryset.filter.assert_called_once_with(post__lte=7)


def test_requesting_next_page_limits_queryset_to_specified_length(mock_queryset):
    page = get_page(mock_queryset, "post", 6, 7)
    assert len(page.object_list) == 6


def test_paginator_returns_empty_first_page_without_errors():
    get_page([], "post", 6)


def test_paginator_raises_empty_page_error_if_nth_page_is_empty(mocker):
    queryset = mocker.Mock(filter=lambda **_: [])
    with pytest.raises(EmptyPage):
        get_page(queryset, "post", 6, 20)


def test_paginator_raises_invalid_page_error_if_starting_position_is_negative():
    with pytest.raises(InvalidPage):
        get_page(None, None, 0, -1)


def test_page_can_be_tested_to_see_if_next_page_exists(mock_objects):
    page = get_page(mock_objects, "post", 6)
    assert page.has_next()


def test_last_page_has_no_next(mock_objects):
    page = get_page([], "post", 6)
    assert not page.next
    assert not page.has_next()


def test_cursor_page_is_first_if_start_is_zero():
    page = CursorPage(0, [])
    assert page.first


def test_cursor_page_is_not_first_if_start_is_not_zero():
    page = CursorPage(1, [])
    assert not page.first
