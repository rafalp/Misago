from unittest.mock import Mock

import pytest

from ..menu import Menu


@pytest.fixture
def menu():
    return Menu()


def test_add_item_adds_item(menu):
    menu.add_item(
        key="test",
        url_name="misago:usercp-edit-details",
        label="Test",
    )

    assert len(menu.items) == 1
    assert menu.items[0].key == "test"


def test_add_item_after_adds_item_in_right_position(menu):
    menu.add_item(
        key="test",
        url_name="misago:usercp-edit-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:usercp-change-username",
        label="Test 2",
    )
    menu.add_item(
        key="test3",
        url_name="misago:usercp-change-email-password",
        label="Test 3",
        after="test",
    )

    assert len(menu.items) == 3
    assert menu.items[0].key == "test"
    assert menu.items[1].key == "test3"
    assert menu.items[2].key == "test2"


def test_add_item_before_adds_item_in_right_position(menu):
    menu.add_item(
        key="test",
        url_name="misago:usercp-edit-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:usercp-change-username",
        label="Test 2",
    )
    menu.add_item(
        key="test3",
        url_name="misago:usercp-change-email-password",
        label="Test 3",
        before="test2",
    )

    assert len(menu.items) == 3
    assert menu.items[0].key == "test"
    assert menu.items[1].key == "test3"
    assert menu.items[2].key == "test2"


def test_add_item_invalid_after_raises_value_error(menu):
    menu.add_item(
        key="test",
        url_name="misago:usercp-edit-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:usercp-change-username",
        label="Test 2",
    )

    with pytest.raises(ValueError) as exc_info:
        menu.add_item(
            key="test3",
            url_name="misago:usercp-change-email-password",
            label="Test 3",
            after="invalid",
        )

    assert "Item with key 'invalid' doesn't exist." == str(exc_info.value)


def test_add_item_invalid_before_raises_value_error(menu):
    menu.add_item(
        key="test",
        url_name="misago:usercp-edit-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:usercp-change-username",
        label="Test 2",
    )

    with pytest.raises(ValueError) as exc_info:
        menu.add_item(
            key="test3",
            url_name="misago:usercp-change-email-password",
            label="Test 3",
            before="invalid",
        )

    assert "Item with key 'invalid' doesn't exist." == str(exc_info.value)


def test_get_items_returns_bound_items(menu):
    menu.add_item(
        key="test",
        url_name="misago:usercp-edit-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:usercp-change-username",
        label="Test 2",
    )
    menu.add_item(
        key="test3",
        url_name="misago:usercp-change-email-password",
        label="Test 3",
    )

    items = menu.get_items(Mock(path_info="/options/change-username/"))

    assert len(items) == 3

    assert not items[0].active
    assert items[0].url == "/options/edit-details/"

    assert items[1].active
    assert items[1].url == "/options/change-username/"

    assert not items[2].active
    assert items[2].url == "/options/sign-in-credentials/"


def test_get_items_filters_items_visibility(menu):
    menu.add_item(
        key="test",
        url_name="misago:usercp-edit-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:usercp-change-username",
        label="Test 2",
        visible=lambda r: r.user is False,
    )
    menu.add_item(
        key="test3",
        url_name="misago:usercp-change-email-password",
        label="Test 3",
        visible=lambda r: r.user,
    )

    items = menu.get_items(Mock(path_info="/options/change-username/", user=False))

    assert len(items) == 2

    assert items[0].key == "test"
    assert not items[0].active
    assert items[0].url == "/options/edit-details/"

    assert items[1].key == "test2"
    assert items[1].active
    assert items[1].url == "/options/change-username/"
