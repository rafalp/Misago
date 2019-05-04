import pytest
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ....test import assert_has_error_message
from ... import THEME_CACHE
from ..css import get_next_css_order

FIRST = 0
MIDDLE = 1
LAST = 2


@pytest.fixture
def css_list(theme):
    return [
        theme.css.create(name="CSS", url="https://test.cdn/font.css", order=FIRST),
        theme.css.create(name="CSS", url="https://test.cdn/font.css", order=MIDDLE),
        theme.css.create(name="CSS", url="https://test.cdn/font.css", order=LAST),
    ]


@pytest.fixture
def move_up(admin_client):
    def move_up_client(theme, css):
        url = reverse(
            "misago:admin:themes:move-css-up", kwargs={"pk": theme.pk, "css_pk": css.pk}
        )
        return admin_client.post(url)

    return move_up_client


@pytest.fixture
def move_down(admin_client):
    def move_down_client(theme, css):
        url = reverse(
            "misago:admin:themes:move-css-down",
            kwargs={"pk": theme.pk, "css_pk": css.pk},
        )
        return admin_client.post(url)

    return move_down_client


def test_first_css_cant_be_moved_up(move_up, theme, css_list):
    first_css = css_list[FIRST]
    move_up(theme, first_css)
    first_css.refresh_from_db()
    assert first_css.order == FIRST


def test_last_css_cant_be_moved_down(move_down, theme, css_list):
    last_css = css_list[LAST]
    move_down(theme, last_css)
    last_css.refresh_from_db()
    assert last_css.order == LAST


def test_first_css_can_be_moved_down(move_down, theme, css_list):
    first_css = css_list[FIRST]
    move_down(theme, first_css)
    first_css.refresh_from_db()
    assert first_css.order == MIDDLE


def test_last_css_can_be_moved_up(move_up, theme, css_list):
    last_css = css_list[LAST]
    move_up(theme, last_css)
    last_css.refresh_from_db()
    assert last_css.order == MIDDLE


def test_middle_css_can_be_moved_down(move_down, theme, css_list):
    middle_css = css_list[MIDDLE]
    move_down(theme, middle_css)
    middle_css.refresh_from_db()
    assert middle_css.order == LAST


def test_middle_css_can_be_moved_up(move_up, theme, css_list):
    middle_css = css_list[MIDDLE]
    move_up(theme, middle_css)
    middle_css.refresh_from_db()
    assert middle_css.order == FIRST


def test_first_css_changes_order_with_middle_css_when_moved_down(
    move_down, theme, css_list
):
    move_down(theme, css_list[FIRST])
    middle_css = css_list[MIDDLE]
    middle_css.refresh_from_db()
    assert middle_css.order == FIRST


def test_last_css_changes_order_with_middle_css_when_moved_up(move_up, theme, css_list):
    move_up(theme, css_list[LAST])
    middle_css = css_list[MIDDLE]
    middle_css.refresh_from_db()
    assert middle_css.order == LAST


def test_middle_css_changes_order_with_last_css_when_moved_down(
    move_down, theme, css_list
):
    move_down(theme, css_list[MIDDLE])
    last_css = css_list[LAST]
    last_css.refresh_from_db()
    assert last_css.order == MIDDLE


def test_middle_css_changes_order_with_first_css_when_moved_up(
    move_up, theme, css_list
):
    move_up(theme, css_list[MIDDLE])
    first_css = css_list[FIRST]
    first_css.refresh_from_db()
    assert first_css.order == MIDDLE


def test_first_css_changes_order_with_last_css_when_moved_down_after_middle_deletion(
    move_down, theme, css_list
):
    css_list[MIDDLE].delete()
    move_down(theme, css_list[FIRST])
    last_css = css_list[LAST]
    last_css.refresh_from_db()
    assert last_css.order == FIRST


def test_last_css_changes_order_with_first_css_when_moved_up_after_middle_deletion(
    move_up, theme, css_list
):
    css_list[MIDDLE].delete()
    move_up(theme, css_list[LAST])
    first_css = css_list[FIRST]
    first_css.refresh_from_db()
    assert first_css.order == LAST


def test_if_css_doesnt_belong_to_theme_move_down_action_sets_error_message(
    move_down, other_theme, css_list
):
    response = move_down(other_theme, css_list[MIDDLE])
    assert_has_error_message(response)


def test_if_css_doesnt_belong_to_theme_move_up_action_sets_error_message(
    move_up, other_theme, css_list
):
    response = move_up(other_theme, css_list[MIDDLE])
    assert_has_error_message(response)


def test_if_ran_for_default_theme_move_down_action_sets_error_message(
    move_down, default_theme, css_list
):
    response = move_down(default_theme, css_list[MIDDLE])
    assert_has_error_message(response)


def test_if_ran_for_default_theme_move_up_action_sets_error_message(
    move_up, default_theme, css_list
):
    response = move_up(default_theme, css_list[MIDDLE])
    assert_has_error_message(response)


def test_if_given_nonexisting_css_id_move_down_action_sets_error_message(
    mocker, move_down, theme, css_list
):
    response = move_down(theme, mocker.Mock(pk=css_list[LAST].pk + 1))
    assert_has_error_message(response)


def test_if_given_nonexisting_css_id_move_up_action_sets_error_message(
    mocker, move_up, theme, css_list
):
    response = move_up(theme, mocker.Mock(pk=css_list[LAST].pk + 1))
    assert_has_error_message(response)


def test_if_given_nonexisting_theme_id_move_down_action_sets_error_message(
    mocker, move_down, nonexisting_theme, css_list
):
    response = move_down(nonexisting_theme, css_list[FIRST])
    assert_has_error_message(response)


def test_if_given_nonexisting_theme_id_move_up_action_sets_error_message(
    mocker, move_up, nonexisting_theme, css_list
):
    response = move_up(nonexisting_theme, css_list[LAST])
    assert_has_error_message(response)


def test_next_new_css_order_is_larger_than_largest_existing_css_order(theme):
    theme.css.create(name="CSS", url="https://test.cdn/font.css", order=4)
    assert get_next_css_order(theme) == 5


def test_moving_css_up_invalidates_theme_cache(move_up, theme, css_list):
    with assert_invalidates_cache(THEME_CACHE):
        move_up(theme, css_list[LAST])


def test_moving_css_down_invalidates_theme_cache(move_down, theme, css_list):
    with assert_invalidates_cache(THEME_CACHE):
        move_down(theme, css_list[FIRST])
