from django.urls import reverse

from ....cache.test import assert_invalidates_cache
from ... import SOCIALAUTH_CACHE


def test_top_provider_can_be_moved_down(admin_client, provider, other_provider):
    provider.order = 0
    provider.save()

    other_provider.order = 1
    other_provider.save()

    admin_client.post(
        reverse("misago:admin:settings:socialauth:down", kwargs={"pk": provider.pk})
    )

    provider.refresh_from_db()
    assert provider.order == 1
    other_provider.refresh_from_db()
    assert other_provider.order == 0


def test_top_provider_cant_be_moved_up(admin_client, provider, other_provider):
    provider.order = 0
    provider.save()

    other_provider.order = 1
    other_provider.save()

    admin_client.post(
        reverse("misago:admin:settings:socialauth:up", kwargs={"pk": provider.pk})
    )

    provider.refresh_from_db()
    assert provider.order == 0
    other_provider.refresh_from_db()
    assert other_provider.order == 1


def test_bottom_provider_cant_be_moved_down(admin_client, provider, other_provider):
    provider.order = 1
    provider.save()

    other_provider.order = 0
    other_provider.save()

    admin_client.post(
        reverse("misago:admin:settings:socialauth:down", kwargs={"pk": provider.pk})
    )

    provider.refresh_from_db()
    assert provider.order == 1
    other_provider.refresh_from_db()
    assert other_provider.order == 0


def test_bottom_provider_can_be_moved_up(admin_client, provider, other_provider):
    provider.order = 1
    provider.save()

    other_provider.order = 0
    other_provider.save()

    admin_client.post(
        reverse("misago:admin:settings:socialauth:up", kwargs={"pk": provider.pk})
    )

    provider.refresh_from_db()
    assert provider.order == 0
    other_provider.refresh_from_db()
    assert other_provider.order == 1


def test_moving_provider_down_invalidates_providers_cache(
    admin_client, provider, other_provider
):
    provider.order = 0
    provider.save()

    other_provider.order = 1
    other_provider.save()

    with assert_invalidates_cache(SOCIALAUTH_CACHE):
        admin_client.post(
            reverse("misago:admin:settings:socialauth:down", kwargs={"pk": provider.pk})
        )


def test_moving_provider_up_invalidates_providers_cache(
    admin_client, provider, other_provider
):
    provider.order = 1
    provider.save()

    other_provider.order = 0
    other_provider.save()

    with assert_invalidates_cache(SOCIALAUTH_CACHE):
        admin_client.post(
            reverse("misago:admin:settings:socialauth:up", kwargs={"pk": provider.pk})
        )


def test_disabled_provider_cant_be_moved_down(
    admin_client, disabled_provider, provider
):
    provider.order = 1
    provider.save()

    disabled_provider.order = 0
    disabled_provider.save()

    admin_client.post(
        reverse(
            "misago:admin:settings:socialauth:down", kwargs={"pk": disabled_provider.pk}
        )
    )

    disabled_provider.refresh_from_db()
    assert disabled_provider.order == 0
    provider.refresh_from_db()
    assert provider.order == 1


def test_disabled_provider_cant_be_moved_up(admin_client, disabled_provider, provider):
    provider.order = 0
    provider.save()

    disabled_provider.order = 1
    disabled_provider.save()

    admin_client.post(
        reverse(
            "misago:admin:settings:socialauth:up", kwargs={"pk": disabled_provider.pk}
        )
    )

    disabled_provider.refresh_from_db()
    assert disabled_provider.order == 1
    provider.refresh_from_db()
    assert provider.order == 0


def test_moving_up_not_setup_provider_has_no_errors(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:socialauth:up", kwargs={"pk": "facebook"})
    )
    assert response.status_code == 302


def test_moving_down_not_setup_provider_has_no_errors(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:socialauth:down", kwargs={"pk": "facebook"})
    )
    assert response.status_code == 302


def test_moving_up_undefined_provider_has_no_errors(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:socialauth:up", kwargs={"pk": "undefined"})
    )
    assert response.status_code == 302


def test_moving_down_undefined_provider_has_no_errors(admin_client):
    response = admin_client.post(
        reverse("misago:admin:settings:socialauth:down", kwargs={"pk": "undefined"})
    )
    assert response.status_code == 302
