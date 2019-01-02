import pytest
from django.urls import reverse

from ....test import assert_contains


@pytest.fixture
def create_link(theme):
    return reverse("misago:admin:appearance:themes:new-css", kwargs={"pk": theme.pk})


@pytest.fixture
def edit_link(theme, css):
    return reverse(
        "misago:admin:appearance:themes:edit-css",
        kwargs={"pk": theme.pk, "css_pk": css.pk},
    )


@pytest.fixture
def data():
    return {"name": "test.css", "source": (".page-header { padding: 0}")}


def test_css_creation_form_is_displayed(admin_client, create_link):
    response = admin_client.get(create_link)
    assert response.status_code == 200
    assert_contains(response, "New CSS")


def test_css_can_be_created(theme, admin_client, create_link, data):
    admin_client.post(create_link, data)
    assert theme.css.exists()


def test_css_is_created_with_entered_name(theme, admin_client, create_link, data):
    admin_client.post(create_link, data)
    assert theme.css.last().name == data["name"]


def test_created_source_file_contains_css_entered_by_user(
    theme, admin_client, create_link, data
):
    admin_client.post(create_link, data)
    css = theme.css.last()
    assert css.source_file.read().decode("utf-8") == data["source"]


def test_source_file_is_created_in_theme_directory(
    theme, admin_client, create_link, data
):
    admin_client.post(create_link, data)
    css = theme.css.last()
    assert theme.dirname in str(css.source_file)


def test_created_source_file_name_starts_with_asset_name(
    theme, admin_client, create_link, data
):
    admin_client.post(create_link, data)
    css = theme.css.last()
    source_filename = str(css.source_file).split("/")[-1]
    assert source_filename.startswith("test.")


def test_created_source_file_has_css_extension(theme, admin_client, create_link, data):
    admin_client.post(create_link, data)
    css = theme.css.last()
    source_filename = str(css.source_file).split("/")[-1]
    assert source_filename.endswith(".css")


def test_created_source_file_is_hashed(theme, admin_client, create_link, data):
    admin_client.post(create_link, data)
    css = theme.css.last()
    source_filename = str(css.source_file).split("/")[-1]
    assert ".%s." % css.source_hash in source_filename


def test_css_creation_fails_if_name_is_not_given(
    theme, admin_client, create_link, data
):
    data["name"] = ""
    admin_client.post(create_link, data)
    assert not theme.css.exists()


def test_css_creation_fails_if_name_is_not_valid(
    theme, admin_client, create_link, data
):
    data["name"] = "missing-extension"
    admin_client.post(create_link, data)
    assert not theme.css.exists()


def test_css_creation_fails_if_name_is_already_taken_by_other_css_in_theme(
    theme, admin_client, create_link, data, css
):
    data["name"] = css.name
    admin_client.post(create_link, data)
    assert theme.css.count() == 1


def test_css_name_usage_check_passess_if_name_is_used_by_other_theme_css(
    other_theme, admin_client, data, css
):
    create_link = reverse(
        "misago:admin:appearance:themes:new-css", kwargs={"pk": other_theme.pk}
    )
    data["name"] = css.name
    admin_client.post(create_link, data)
    assert other_theme.css.exists()


def test_css_creation_fails_if_source_is_not_given(
    theme, admin_client, create_link, data
):
    data["source"] = ""
    admin_client.post(create_link, data)
    assert not theme.css.exists()


def test_css_creation_form_redirects_user_to_edition_after_creation(
    theme, admin_client, create_link, data
):
    data["stay"] = "1"
    response = admin_client.post(create_link, data)
    assert response["location"] == reverse(
        "misago:admin:appearance:themes:edit-css",
        kwargs={"pk": theme.pk, "css_pk": theme.css.last().pk},
    )


def test_css_edition_form_is_displayed(admin_client, edit_link, css):
    response = admin_client.get(edit_link)
    assert response.status_code == 200
    assert_contains(response, css.name)


def test_css_edition_form_contains_source_file_contents(admin_client, edit_link, css):
    response = admin_client.get(edit_link)
    assert_contains(response, css.source_file.read().decode("utf-8"))


def test_name_can_be_changed(admin_client, edit_link, css, data):
    data["name"] = "new-name.css"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert css.name == data["name"]


def test_name_change_also_changes_source_file_name(admin_client, edit_link, css, data):
    data["name"] = "new-name.css"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert "new-name" in str(css.source_file)


def test_css_source_can_be_changed(admin_client, edit_link, css, data):
    data["source"] = ".misago-footer { display: none; }"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert css.source_file.read().decode("utf-8") == data["source"]
