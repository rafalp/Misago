import pytest
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ....test import assert_contains, assert_has_error_message
from ... import THEME_CACHE
from ...models import Theme


@pytest.fixture
def create_link():
    return reverse("misago:admin:themes:new")


@pytest.fixture
def edit_link(theme):
    return reverse("misago:admin:themes:edit", kwargs={"pk": theme.pk})


def test_theme_creation_form_is_displayed(admin_client, create_link):
    response = admin_client.get(create_link)
    assert response.status_code == 200
    assert_contains(response, "New theme")


def test_theme_creation_form_reads_parent_from_url_and_preselects_it_in_parent_select(
    admin_client, create_link, theme
):
    response = admin_client.get("%s?parent=%s" % (create_link, theme.pk))
    assert_contains(response, '<option value="%s" selected>' % theme.pk)


def test_theme_creation_form_reads_parent_from_url_and_discards_invalid_value(
    admin_client, create_link, theme
):
    response = admin_client.get("%s?parent=%s" % (create_link, theme.pk + 1))
    assert response.status_code == 200


def test_theme_can_be_created(admin_client, create_link):
    admin_client.post(create_link, {"name": "New Theme"})
    Theme.objects.get(name="New Theme")


def test_child_theme_for_custom_theme_can_be_created(admin_client, create_link, theme):
    admin_client.post(create_link, {"name": "New Theme", "parent": theme.pk})
    child_theme = Theme.objects.get(name="New Theme")
    assert child_theme.parent == theme


def test_child_theme_for_default_theme_can_be_created(
    admin_client, create_link, default_theme
):
    admin_client.post(create_link, {"name": "New Theme", "parent": default_theme.pk})
    child_theme = Theme.objects.get(name="New Theme")
    assert child_theme.parent == default_theme


def test_creating_child_theme_updates_themes_tree(admin_client, create_link, theme):
    admin_client.post(create_link, {"name": "New Theme", "parent": theme.pk})

    child_theme = Theme.objects.get(name="New Theme")
    assert child_theme.tree_id == theme.tree_id
    assert child_theme.lft == 2
    assert child_theme.rght == 3

    theme.refresh_from_db()
    assert theme.lft == 1
    assert theme.rght == 4


def test_theme_creation_fails_if_name_is_not_given(admin_client, create_link):
    admin_client.post(create_link, {"name": ""})
    assert Theme.objects.count() == 1


def test_theme_creation_fails_if_parent_theme_doesnt_exist(
    admin_client, create_link, nonexisting_theme
):
    admin_client.post(
        create_link, {"name": "New Theme", "parent": nonexisting_theme.pk}
    )
    assert Theme.objects.count() == 1


def test_theme_edition_form_is_displayed(admin_client, edit_link, theme):
    response = admin_client.get(edit_link)
    assert response.status_code == 200
    assert_contains(response, theme.name)


def test_theme_name_can_be_edited(admin_client, edit_link, theme):
    admin_client.post(edit_link, {"name": "Edited Theme"})
    theme.refresh_from_db()
    assert theme.name == "Edited Theme"


def test_theme_can_be_moved_under_other_theme(
    admin_client, edit_link, theme, default_theme
):
    admin_client.post(edit_link, {"name": theme.name, "parent": default_theme.pk})
    theme.refresh_from_db()
    assert theme.parent == default_theme


def test_moving_theme_under_other_theme_updates_themes_tree(
    admin_client, edit_link, theme, default_theme
):
    admin_client.post(edit_link, {"name": theme.name, "parent": default_theme.pk})

    default_theme.refresh_from_db()
    theme.refresh_from_db()

    assert theme.tree_id == default_theme.tree_id
    assert theme.lft == 2
    assert theme.rght == 3

    assert default_theme.lft == 1
    assert default_theme.rght == 4


def test_theme_cant_be_moved_under_itself(admin_client, edit_link, theme):
    admin_client.post(edit_link, {"name": theme.name, "parent": theme.pk})
    theme.refresh_from_db()
    assert not theme.parent


def test_theme_cant_be_moved_under_its_child_theme(admin_client, edit_link, theme):
    child_theme = Theme.objects.create(name="Child Theme", parent=theme)
    admin_client.post(edit_link, {"name": theme.name, "parent": child_theme.pk})
    theme.refresh_from_db()
    assert not theme.parent


def test_moving_child_theme_under_other_theme_updates_both_themes_trees(
    admin_client, theme, default_theme
):
    child_theme = Theme.objects.create(name="Child Theme", parent=theme)
    edit_link = reverse("misago:admin:themes:edit", kwargs={"pk": child_theme.pk})

    admin_client.post(edit_link, {"name": child_theme.name, "parent": default_theme.pk})

    default_theme.refresh_from_db()
    child_theme.refresh_from_db()
    theme.refresh_from_db()

    assert child_theme.parent == default_theme
    assert child_theme.tree_id == default_theme.tree_id
    assert child_theme.lft == 2
    assert child_theme.rght == 3

    assert default_theme.lft == 1
    assert default_theme.rght == 4

    assert theme.tree_id != default_theme.tree_id
    assert theme.lft == 1
    assert theme.rght == 2


def test_moving_theme_under_root_updates_theme_tree_and_creates_new_one(
    admin_client, edit_link, theme, default_theme
):
    theme.parent = default_theme
    theme.save()

    admin_client.post(edit_link, {"name": theme.name})

    default_theme.refresh_from_db()
    theme.refresh_from_db()

    assert theme.parent is None
    assert theme.tree_id != default_theme.tree_id
    assert theme.lft == 1
    assert theme.rght == 2

    assert default_theme.lft == 1
    assert default_theme.rght == 2


def test_moving_theme_with_child_under_root_updates_theme_tree_and_creates_new_one(
    admin_client, edit_link, theme, default_theme
):
    theme.parent = default_theme
    theme.save()

    child_theme = Theme.objects.create(name="Child Theme", parent=theme)

    admin_client.post(edit_link, {"name": theme.name})

    default_theme.refresh_from_db()
    child_theme.refresh_from_db()
    theme.refresh_from_db()

    assert theme.tree_id != default_theme.tree_id
    assert theme.lft == 1
    assert theme.rght == 4

    assert child_theme.parent == theme
    assert child_theme.tree_id == theme.tree_id
    assert child_theme.lft == 2
    assert child_theme.rght == 3

    assert default_theme.lft == 1
    assert default_theme.rght == 2


def test_theme_edition_fails_if_parent_theme_doesnt_exist(
    admin_client, edit_link, theme, nonexisting_theme
):
    admin_client.post(
        edit_link, {"name": "Edited Theme", "parent": nonexisting_theme.pk}
    )
    theme.refresh_from_db()
    assert theme.name != "Edited Theme"


def test_error_message_is_set_if_user_attempts_to_edit_default_theme(
    admin_client, default_theme
):
    edit_link = reverse("misago:admin:themes:edit", kwargs={"pk": default_theme.pk})
    response = admin_client.get(edit_link)
    assert_has_error_message(response)


def test_error_message_is_set_if_user_attempts_to_edit_nonexisting_theme(
    admin_client, nonexisting_theme
):
    edit_link = reverse("misago:admin:themes:edit", kwargs={"pk": nonexisting_theme.pk})
    response = admin_client.get(edit_link)
    assert_has_error_message(response)


def test_moving_theme_invalidates_themes_cache(
    admin_client, edit_link, theme, default_theme
):
    with assert_invalidates_cache(THEME_CACHE):
        admin_client.post(edit_link, {"name": theme.name, "parent": default_theme.pk})
