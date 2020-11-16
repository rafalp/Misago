import pytest
from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ... import SOCIALAUTH_CACHE


@pytest.fixture
def admin_link(provider):
    return reverse(
        "misago:admin:settings:socialauth:disable", kwargs={"pk": provider.pk}
    )


def test_provider_can_be_disabled(admin_client, admin_link, provider):
    admin_client.post(admin_link)
    provider.refresh_from_db()
    assert not provider.is_active


def test_disabling_provider_invalidates_cache(admin_client, admin_link):
    with assert_invalidates_cache(SOCIALAUTH_CACHE):
        admin_client.post(admin_link)


def test_already_disabled_provider_cant_be_disabled(admin_client, disabled_provider):
    admin_link = reverse(
        "misago:admin:settings:socialauth:disable", kwargs={"pk": disabled_provider.pk}
    )
    admin_client.post(admin_link)
    disabled_provider.refresh_from_db()
    assert not disabled_provider.is_active


def test_provider_that_wasnt_setup_yet_cant_be_disabled(admin_client):
    admin_link = reverse(
        "misago:admin:settings:socialauth:disable", kwargs={"pk": "github"}
    )
    response = admin_client.post(admin_link)
    assert response.status_code == 302


def test_undefined_provider_cant_be_disabled(admin_client):
    admin_link = reverse(
        "misago:admin:settings:socialauth:disable", kwargs={"pk": "undefined"}
    )
    response = admin_client.post(admin_link)
    assert response.status_code == 302
