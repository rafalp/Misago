import pytest
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ....test import assert_contains, assert_has_error_message
from ... import THEME_CACHE


@pytest.fixture
def create_link(theme):
    return reverse("misago:admin:themes:new-css-link", kwargs={"pk": theme.pk})


@pytest.fixture
def edit_link(theme, css_link):
    return reverse(
        "misago:admin:themes:edit-css-link",
        kwargs={"pk": theme.pk, "css_pk": css_link.pk},
    )


@pytest.fixture
def data():
    return {"name": "CSS link", "url": "https://example.com/cdn.css"}


def test_css_link_creation_form_is_displayed(admin_client, create_link):
    response = admin_client.get(create_link)
    assert response.status_code == 200
    assert_contains(response, "New CSS link")


def test_css_link_can_be_created(theme, admin_client, create_link, data):
    admin_client.post(create_link, data)
    assert theme.css.exists()


def test_css_link_is_created_with_entered_name(theme, admin_client, create_link, data):
    admin_client.post(create_link, data)
    assert theme.css.last().name == data["name"]


def test_css_link_name_can_be_descriptive(theme, admin_client, create_link, data):
    data["name"] = "font (from font.hosting.com)"
    admin_client.post(create_link, data)
    assert theme.css.last().name == data["name"]


def test_css_link_creation_fails_if_name_is_not_given(
    theme, admin_client, create_link, data
):
    data["name"] = ""
    admin_client.post(create_link, data)
    assert not theme.css.exists()


def test_css_link_creation_fails_if_name_is_already_taken_by_other_css_in_theme(
    theme, admin_client, create_link, data, css
):
    data["name"] = css.name
    admin_client.post(create_link, data)
    assert theme.css.count() == 1


def test_css_link_name_usage_check_passess_if_name_is_used_by_other_theme_css(
    other_theme, admin_client, data, css
):
    create_link = reverse(
        "misago:admin:themes:new-css-link", kwargs={"pk": other_theme.pk}
    )
    data["name"] = css.name
    admin_client.post(create_link, data)
    assert other_theme.css.exists()


def test_css_link_creation_fails_if_url_is_not_given(
    theme, admin_client, create_link, data
):
    data["url"] = ""
    admin_client.post(create_link, data)
    assert not theme.css.exists()


def test_css_link_creation_fails_if_url_is_not_valid(
    theme, admin_client, create_link, data
):
    data["url"] = "invalid-url"
    admin_client.post(create_link, data)
    assert not theme.css.exists()


def test_css_link_is_created_with_correct_order(
    theme, admin_client, create_link, css, data
):
    admin_client.post(create_link, data)
    css_link = theme.css.get(name=data["name"])
    assert css_link.order == 1


def test_css_link_creation_queues_task_to_download_remote_css_size(
    theme, admin_client, create_link, data, mock_update_remote_css_size
):
    admin_client.post(create_link, data)
    css_link = theme.css.last()
    mock_update_remote_css_size.assert_called_once_with(css_link.pk)


def test_css_link_creation_invalidates_theme_cache(
    theme, admin_client, create_link, data
):
    with assert_invalidates_cache(THEME_CACHE):
        admin_client.post(create_link, data)


def test_error_message_is_set_if_user_attempts_to_create_css_link_in_default_theme(
    default_theme, admin_client
):
    create_link = reverse(
        "misago:admin:themes:new-css-link", kwargs={"pk": default_theme.pk}
    )
    response = admin_client.get(create_link)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_create_css_link_in_nonexisting_theme(
    nonexisting_theme, admin_client
):
    create_link = reverse(
        "misago:admin:themes:new-css-link", kwargs={"pk": nonexisting_theme.pk}
    )
    response = admin_client.get(create_link)
    assert_has_error_message(response)


def test_css_link_creation_form_redirects_user_to_new_creation_form_after_creation(
    theme, admin_client, create_link, data
):
    data["stay"] = "1"
    response = admin_client.post(create_link, data)
    assert response["location"] == reverse(
        "misago:admin:themes:new-css-link", kwargs={"pk": theme.pk}
    )


def test_css_link_edition_form_is_displayed(admin_client, edit_link, css_link):
    response = admin_client.get(edit_link)
    assert response.status_code == 200
    assert_contains(response, css_link.name)


def test_css_link_name_can_be_changed(admin_client, edit_link, css_link, data):
    data["name"] = "new link name"
    admin_client.post(edit_link, data)

    css_link.refresh_from_db()
    assert css_link.name == data["name"]


def test_css_link_url_can_be_changed(admin_client, edit_link, css_link, data):
    data["url"] = "https://new.css-link.com/test.css"
    admin_client.post(edit_link, data)

    css_link.refresh_from_db()
    assert css_link.url == data["url"]


def test_changing_css_link_url_queues_task_to_download_remote_css_size(
    admin_client, edit_link, css_link, data, mock_update_remote_css_size
):
    data["url"] = "https://new.css-link.com/test.css"
    admin_client.post(edit_link, data)
    css_link.refresh_from_db()
    mock_update_remote_css_size.assert_called_once_with(css_link.pk)


def test_not_changing_css_link_url_doesnt_queue_task_to_download_remote_css_size(
    admin_client, edit_link, css_link, data, mock_update_remote_css_size
):
    admin_client.post(edit_link, data)
    css_link.refresh_from_db()
    mock_update_remote_css_size.assert_not_called()


def test_changing_css_link_invalidates_theme_cache(admin_client, edit_link, data):
    with assert_invalidates_cache(THEME_CACHE):
        admin_client.post(edit_link, data)


def test_css_order_stays_the_same_after_edit(admin_client, edit_link, css_link, data):
    original_order = css_link.order
    data["name"] = "changed link"
    admin_client.post(edit_link, data)

    css_link.refresh_from_db()
    assert css_link.order == original_order


def test_error_message_is_set_if_user_attempts_to_edit_css_file_with_link_form(
    theme, admin_client, css
):
    edit_link = reverse(
        "misago:admin:themes:edit-css-link", kwargs={"pk": theme.pk, "css_pk": css.pk}
    )
    response = admin_client.get(edit_link)
    assert_has_error_message(response)
