import pytest
from django.urls import reverse

from ...models import SocialAuthProvider


admin_link = reverse("misago:admin:settings:socialauth:edit", kwargs={"pk": "facebook"})


@pytest.fixture
def provider(db):
    return SocialAuthProvider.objects.create(
        provider="facebook", is_active=True, order=0
    )


def test_facebook_form_can_be_accessed(admin_client):
    response = admin_client.get(admin_link)
    assert response.status_code == 200


def test_facebook_login_can_be_setup(admin_client):
    admin_client.post(
        admin_link,
        {
            "is_active": "1",
            "associate_by_email": "1",
            "key": "test-key",
            "secret": "test-secret",
        },
    )

    provider = SocialAuthProvider.objects.get(provider="facebook")
    assert provider.is_active
    assert provider.settings == {
        "associate_by_email": 1,
        "key": "test-key",
        "secret": "test-secret",
    }


def test_facebook_login_can_be_disabled(admin_client, provider):
    admin_client.post(admin_link, {"is_active": "0"})

    provider = SocialAuthProvider.objects.get(provider="facebook")
    assert not provider.is_active


def test_facebook_login_form_requires_key_to_setup(admin_client):
    admin_client.post(admin_link, {"is_active": "1", "secret": "test-secret"})

    with pytest.raises(SocialAuthProvider.DoesNotExist):
        SocialAuthProvider.objects.get(provider="facebook")


def test_facebook_login_form_requires_secret_to_setup(admin_client):
    admin_client.post(admin_link, {"is_active": "1", "key": "test-key"})

    with pytest.raises(SocialAuthProvider.DoesNotExist):
        SocialAuthProvider.objects.get(provider="facebook")
