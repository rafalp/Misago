from unittest.mock import Mock

import pytest

from .pagenav import PageNav


@pytest.fixture
def pagenav():
    return PageNav()


def test_add_item_adds_item(pagenav):
    pagenav.add_item(
        key="test",
        url="/test/",
        label="Test",
    )

    assert len(pagenav.items) == 1
    assert pagenav.items[0].key == "test"


def test_add_item_after_adds_item_in_right_position(pagenav):
    pagenav.add_item(
        key="test",
        url="/test/",
        label="Test",
    )
    pagenav.add_item(
        key="test2",
        url="/test-2/",
        label="Test 2",
    )
    pagenav.add_item(
        key="test3",
        url="/test-3/",
        label="Test 3",
        after="test",
    )

    assert len(pagenav.items) == 3
    assert pagenav.items[0].key == "test"
    assert pagenav.items[1].key == "test3"
    assert pagenav.items[2].key == "test2"


def test_add_item_before_adds_item_in_right_position(pagenav):
    pagenav.add_item(
        key="test",
        url="/test/",
        label="Test",
    )
    pagenav.add_item(
        key="test2",
        url="/test-2/",
        label="Test 2",
    )
    pagenav.add_item(
        key="test3",
        url="/test-3/",
        label="Test 3",
        before="test2",
    )

    assert len(pagenav.items) == 3
    assert pagenav.items[0].key == "test"
    assert pagenav.items[1].key == "test3"
    assert pagenav.items[2].key == "test2"


def test_add_item_invalid_after_raises_value_error(pagenav):
    pagenav.add_item(
        key="test",
        url="/test/",
        label="Test",
    )
    pagenav.add_item(
        key="test2",
        url="/test-2/",
        label="Test 2",
    )

    with pytest.raises(ValueError) as exc_info:
        pagenav.add_item(
            key="test3",
            url="/test-3/",
            label="Test 3",
            after="invalid",
        )

    assert "Item with key 'invalid' doesn't exist." == str(exc_info.value)


def test_add_item_invalid_before_raises_value_error(pagenav):
    pagenav.add_item(
        key="test",
        url="/test/",
        label="Test",
    )
    pagenav.add_item(
        key="test2",
        url="/test-2/",
        label="Test 2",
    )

    with pytest.raises(ValueError) as exc_info:
        pagenav.add_item(
            key="test3",
            url="/test-3/",
            label="Test 3",
            before="invalid",
        )

    assert "Item with key 'invalid' doesn't exist." == str(exc_info.value)


def test_get_items_returns_bound_items(pagenav):
    pagenav.add_item(
        key="test",
        url="/test/",
        label="Test",
    )
    pagenav.add_item(
        key="test2",
        url="/test-2/",
        label="Test 2",
    )
    pagenav.add_item(
        key="test3",
        url="/test-3/",
        label="Test 3",
    )

    items = pagenav.get_items(Mock(path_info="/test-2/"))

    assert len(items) == 3
    assert not items[0].active
    assert items[1].active
    assert not items[2].active
