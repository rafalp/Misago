import pytest
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ....test import assert_has_error_message
from ... import THEME_CACHE
from ...models import Theme


@pytest.fixture
def activate_link(theme):
    return reverse("misago:admin:themes:activate", kwargs={"pk": theme.pk})


def test_active_theme_can_changed(admin_client, activate_link, theme):
    admin_client.post(activate_link)
    theme.refresh_from_db()
    assert theme.is_active


def test_default_theme_can_be_set_as_active_theme(admin_client, default_theme):
    activate_link = reverse(
        "misago:admin:themes:activate", kwargs={"pk": default_theme.pk}
    )
    admin_client.post(activate_link)
    default_theme.refresh_from_db()
    assert default_theme.is_active


def test_changing_active_theme_removes_active_status_from_previous_active_theme(
    admin_client, activate_link, theme
):
    admin_client.post(activate_link)
    # objets.get() will raise if more than one theme is active
    assert Theme.objects.get(is_active=True) == theme


def test_changing_active_theme_to_nonexisting_theme_sets_error_message(
    admin_client, nonexisting_theme
):
    activate_link = reverse(
        "misago:admin:themes:activate", kwargs={"pk": nonexisting_theme.pk}
    )
    response = admin_client.post(activate_link)
    assert_has_error_message(response)


def test_changing_active_theme_invalidates_themes_cache(admin_client, activate_link):
    with assert_invalidates_cache(THEME_CACHE):
        admin_client.post(activate_link)
