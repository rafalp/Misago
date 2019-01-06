import pytest
from django.urls import reverse

from ....test import assert_contains, assert_not_contains
from ...models import Theme


@pytest.fixture
def create_link():
    return reverse("misago:admin:appearance:themes:new")


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


def test_theme_can_be_created(
    admin_client, create_link
):
    admin_client.post(create_link, {"name": "New Theme"})
    Theme.objects.get(name="New Theme")


def test_child_theme_for_custom_theme_can_be_created(
    admin_client, create_link, theme
):
    admin_client.post(create_link, {"name": "New Theme", "parent": theme.pk})
    child_theme = Theme.objects.get(name="New Theme")
    assert child_theme.parent == theme


def test_child_theme_for_default_theme_can_be_created(
    admin_client, create_link, default_theme
):
    admin_client.post(create_link, {"name": "New Theme", "parent": default_theme.pk})
    child_theme = Theme.objects.get(name="New Theme")
    assert child_theme.parent == default_theme


def test_creating_child_theme_updates_themes_tree(
    admin_client, create_link, theme
):
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
