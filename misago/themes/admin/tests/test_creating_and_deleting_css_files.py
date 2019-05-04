import pytest
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ....test import assert_contains, assert_has_error_message
from ... import THEME_CACHE


@pytest.fixture
def create_link(theme):
    return reverse("misago:admin:themes:new-css-file", kwargs={"pk": theme.pk})


@pytest.fixture
def edit_link(theme, css):
    return reverse(
        "misago:admin:themes:edit-css-file", kwargs={"pk": theme.pk, "css_pk": css.pk}
    )


@pytest.fixture
def data():
    return {"name": "test.css", "source": ".page-header { padding: 0}"}


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
        "misago:admin:themes:new-css-file", kwargs={"pk": other_theme.pk}
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


def test_css_file_without_url_is_created_without_rebuilding_flag(
    theme, admin_client, create_link, data
):
    admin_client.post(create_link, data)
    css = theme.css.last()
    assert not css.source_needs_building


def test_css_file_with_image_url_is_created_with_rebuilding_flag(
    theme, admin_client, create_link, data, image
):
    data["source"] = "body { background-image: url(/static/%s); }" % image.name
    admin_client.post(create_link, data)
    css = theme.css.last()
    assert css.source_needs_building


def test_creating_css_file_without_image_url_doesnt_trigger_single_css_file_rebuild(
    theme, admin_client, create_link, data, image, mock_build_single_theme_css
):
    admin_client.post(create_link, data)
    mock_build_single_theme_css.assert_not_called()


def test_creating_css_file_with_image_url_triggers_single_css_file_rebuild(
    theme, admin_client, create_link, data, image, mock_build_single_theme_css
):
    data["source"] = "body { background-image: url(/static/%s); }" % image.name
    admin_client.post(create_link, data)
    css = theme.css.last()

    mock_build_single_theme_css.assert_called_once_with(css.pk)


def test_css_file_is_created_with_correct_order(
    theme, admin_client, create_link, css_link, data
):
    admin_client.post(create_link, data)
    css = theme.css.get(name=data["name"])
    assert css.order == 1


def test_creating_css_file_invalidates_theme_cache(admin_client, create_link, data):
    with assert_invalidates_cache(THEME_CACHE):
        admin_client.post(create_link, data)


def test_error_message_is_set_if_user_attempts_to_create_css_in_default_theme(
    default_theme, admin_client
):
    create_link = reverse(
        "misago:admin:themes:new-css-file", kwargs={"pk": default_theme.pk}
    )
    response = admin_client.get(create_link)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_create_css_in_nonexisting_theme(
    nonexisting_theme, admin_client
):
    create_link = reverse(
        "misago:admin:themes:new-css-file", kwargs={"pk": nonexisting_theme.pk}
    )
    response = admin_client.get(create_link)
    assert_has_error_message(response)


def test_css_creation_form_redirects_user_to_edition_after_creation(
    theme, admin_client, create_link, data
):
    data["stay"] = "1"
    response = admin_client.post(create_link, data)
    assert response["location"] == reverse(
        "misago:admin:themes:edit-css-file",
        kwargs={"pk": theme.pk, "css_pk": theme.css.last().pk},
    )


def test_css_edition_form_is_displayed(admin_client, edit_link, css):
    response = admin_client.get(edit_link)
    assert response.status_code == 200
    assert_contains(response, css.name)


def test_css_edition_form_contains_source_file_contents(admin_client, edit_link, css):
    response = admin_client.get(edit_link)
    assert_contains(response, css.source_file.read().decode("utf-8"))


def test_css_name_can_be_changed(admin_client, edit_link, css, data):
    data["name"] = "new-name.css"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert css.name == data["name"]


def test_css_name_change_also_changes_source_file_name(
    admin_client, edit_link, css, data
):
    data["name"] = "new-name.css"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert "new-name" in str(css.source_file)


def test_css_source_can_be_changed(admin_client, edit_link, css, data):
    data["source"] = ".misago-footer { display: none; }"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert css.source_file.read().decode("utf-8") == data["source"]


def test_changing_css_source_also_changes_source_hash(
    admin_client, edit_link, css, data
):
    original_hash = css.source_hash
    data["source"] = ".misago-footer { display: none; }"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert css.source_hash != original_hash


def test_changing_css_source_also_changes_hash_in_filename(
    admin_client, edit_link, css, data
):
    original_hash = css.source_hash
    data["source"] = ".misago-footer { display: none; }"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert original_hash not in str(css.source_file)
    assert css.source_hash in str(css.source_file)


def test_hash_stays_same_if_source_is_not_changed(admin_client, edit_link, css, data):
    original_hash = css.source_hash
    data["name"] = "changed.css"
    data["source"] = css.source_file.read().decode("utf-8")
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert original_hash == css.source_hash


def test_file_is_not_updated_if_form_data_has_no_changes(
    admin_client, edit_link, css, data
):
    original_source_file = str(css.source_file)
    data["name"] = css.name
    data["source"] = css.source_file.read().decode("utf-8")
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert original_source_file == str(css.source_file)


def test_adding_image_url_to_edited_file_sets_rebuilding_flag(
    theme, admin_client, edit_link, css, data, image
):
    data["source"] = "body { background-image: url(/static/%s); }" % image.name
    admin_client.post(edit_link, data)
    css.refresh_from_db()
    assert css.source_needs_building


def test_removing_url_from_edited_file_removes_rebuilding_flag(
    theme, admin_client, edit_link, css, data
):
    css.source_needs_building = True
    css.save()

    data["source"] = "body { background-image: none; }"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert not css.source_needs_building


def test_adding_image_url_to_edited_file_triggers_single_css_file_rebuild(
    theme, admin_client, edit_link, css, data, image, mock_build_single_theme_css
):
    data["source"] = "body { background-image: url(/static/%s); }" % image.name
    admin_client.post(edit_link, data)

    mock_build_single_theme_css.assert_called_once_with(css.pk)


def test_removing_url_from_edited_file_deosnt_trigger_single_css_file_rebuild(
    theme, admin_client, edit_link, css, data, mock_build_single_theme_css
):
    data["source"] = "body { background-image: none; }"
    admin_client.post(edit_link, data)
    mock_build_single_theme_css.assert_not_called()


def test_css_order_stays_the_same_after_edit(admin_client, edit_link, css, data):
    original_order = css.order
    data["name"] = "changed.css"
    admin_client.post(edit_link, data)

    css.refresh_from_db()
    assert css.order == original_order


def test_editing_css_file_invalidates_theme_cache(admin_client, edit_link, css, data):
    with assert_invalidates_cache(THEME_CACHE):
        admin_client.post(edit_link, data)


def test_css_edit_form_redirects_user_to_edition_after_saving(
    theme, admin_client, edit_link, css, data
):
    data["stay"] = "1"
    response = admin_client.post(edit_link, data)
    assert response["location"] == edit_link


def test_error_message_is_set_if_user_attempts_to_edit_css_file_in_default_theme(
    default_theme, admin_client
):
    edit_link = reverse(
        "misago:admin:themes:edit-css-file",
        kwargs={"pk": default_theme.pk, "css_pk": 1},
    )
    response = admin_client.get(edit_link)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_edit_css_file_in_nonexisting_theme(
    nonexisting_theme, admin_client
):
    edit_link = reverse(
        "misago:admin:themes:edit-css-file",
        kwargs={"pk": nonexisting_theme.pk, "css_pk": 1},
    )
    response = admin_client.get(edit_link)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_edit_css_belonging_to_other_theme(
    other_theme, admin_client, css
):
    edit_link = reverse(
        "misago:admin:themes:edit-css-file",
        kwargs={"pk": other_theme.pk, "css_pk": css.pk},
    )
    response = admin_client.get(edit_link)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_edit_nonexisting_css(
    theme, admin_client
):
    edit_link = reverse(
        "misago:admin:themes:edit-css-file", kwargs={"pk": theme.pk, "css_pk": 1}
    )
    response = admin_client.get(edit_link)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_edit_css_link_with_file_form(
    theme, admin_client, css_link
):
    edit_link = reverse(
        "misago:admin:themes:edit-css-file",
        kwargs={"pk": theme.pk, "css_pk": css_link.pk},
    )
    response = admin_client.get(edit_link)
    assert_has_error_message(response)
