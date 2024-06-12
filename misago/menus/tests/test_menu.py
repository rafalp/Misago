from unittest.mock import Mock

import pytest

from ..menu import Menu


@pytest.fixture
def menu():
    return Menu()


def test_add_item_adds_item(menu):
    menu.add_item(
        key="test",
        url_name="misago:account-details",
        label="Test",
    )

    assert len(menu.items) == 1
    assert menu.items[0].key == "test"


def test_add_item_after_adds_item_in_right_position(menu):
    menu.add_item(
        key="test",
        url_name="misago:account-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:account-username",
        label="Test 2",
    )
    menu.add_item(
        key="test3",
        url_name="misago:account-email",
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
        url_name="misago:account-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:account-username",
        label="Test 2",
    )
    menu.add_item(
        key="test3",
        url_name="misago:account-email",
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
        url_name="misago:account-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:account-username",
        label="Test 2",
    )

    with pytest.raises(ValueError) as exc_info:
        menu.add_item(
            key="test3",
            url_name="misago:account-email",
            label="Test 3",
            after="invalid",
        )

    assert "Item with key 'invalid' doesn't exist." == str(exc_info.value)


def test_add_item_invalid_before_raises_value_error(menu):
    menu.add_item(
        key="test",
        url_name="misago:account-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:account-username",
        label="Test 2",
    )

    with pytest.raises(ValueError) as exc_info:
        menu.add_item(
            key="test3",
            url_name="misago:account-email",
            label="Test 3",
            before="invalid",
        )

    assert "Item with key 'invalid' doesn't exist." == str(exc_info.value)


def test_bind_to_request_returns_bound_menu(menu):
    menu.add_item(
        key="test",
        url_name="misago:account-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:account-username",
        label="Test 2",
    )
    menu.add_item(
        key="test3",
        url_name="misago:account-email",
        label="Test 3",
    )

    bound_menu = menu.bind_to_request(Mock(path_info="/account/username/"))

    assert bound_menu.active.url == "/account/username/"

    assert len(bound_menu.items) == 3

    assert not bound_menu.items[0].active
    assert bound_menu.items[0].url == "/account/details/"

    assert bound_menu.items[1].active
    assert bound_menu.items[1].url == "/account/username/"

    assert not bound_menu.items[2].active
    assert bound_menu.items[2].url == "/account/email/"


def test_bind_to_request__filters_items_visibility(menu):
    menu.add_item(
        key="test",
        url_name="misago:account-details",
        label="Test",
    )
    menu.add_item(
        key="test2",
        url_name="misago:account-username",
        label="Test 2",
        visible=lambda r: r.user is False,
    )
    menu.add_item(
        key="test3",
        url_name="misago:account-email",
        label="Test 3",
        visible=lambda r: r.user,
    )

    bound_menu = menu.bind_to_request(Mock(path_info="/account/username/", user=False))

    assert bound_menu.active.url == "/account/username/"

    assert len(bound_menu.items) == 2

    assert bound_menu.items[0].key == "test"
    assert not bound_menu.items[0].active
    assert bound_menu.items[0].url == "/account/details/"

    assert bound_menu.items[1].key == "test2"
    assert bound_menu.items[1].active
    assert bound_menu.items[1].url == "/account/username/"
