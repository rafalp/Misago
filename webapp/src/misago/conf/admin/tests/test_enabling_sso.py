from django.urls import reverse

from ...models import Setting

admin_link = reverse("misago:admin:settings:sso:index")


def test_sso_form_generates_public_key_when_enabling_sso(admin_client):
    response = admin_client.post(
        admin_link, {"enable_sso": "1", "sso_url": "https://test.com"}
    )
    setting = Setting.objects.get(setting="sso_public_key")
    assert setting.value


def test_sso_form_generates_private_key_when_enabling_sso(admin_client):
    response = admin_client.post(
        admin_link, {"enable_sso": "1", "sso_url": "https://test.com"}
    )
    setting = Setting.objects.get(setting="sso_private_key")
    assert setting.value


def test_sso_public_key_can_be_set_explicitly_when_enabling_sso(admin_client):
    response = admin_client.post(
        admin_link,
        {"enable_sso": "1", "sso_public_key": "custom", "sso_url": "https://test.com"},
    )
    setting = Setting.objects.get(setting="sso_public_key")
    assert setting.value == "custom"


def test_sso_private_key_can_be_set_explicitly_when_enabling_sso(admin_client):
    response = admin_client.post(
        admin_link,
        {"enable_sso": "1", "sso_private_key": "custom", "sso_url": "https://test.com"},
    )
    setting = Setting.objects.get(setting="sso_private_key")
    assert setting.value == "custom"


def test_form_requires_sso_url_when_enabling_sso(admin_client):
    response = admin_client.post(
        admin_link, {"enable_sso": "1", "sso_private_key": "custom", "sso_url": ""}
    )
    setting = Setting.objects.get(setting="enable_sso")
    assert not setting.value
