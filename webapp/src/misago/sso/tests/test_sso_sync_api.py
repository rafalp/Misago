import jwt
from django.contrib.auth import get_user_model
from django.urls import reverse

from ...conf.test import override_dynamic_settings
from .utils import TEST_SSO_SETTINGS

User = get_user_model()
api_link = reverse("simple-sso-sync")


@override_dynamic_settings(enable_sso=False)
def test_sso_api_returns_404_if_sso_is_disabled(db, client):
    response = client.post(api_link)
    assert response.status_code == 404


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_api_returns_400_if_api_request_is_missing_access_token(db, client):
    response = client.post(api_link)
    assert response.status_code == 400


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_api_returns_400_if_access_token_is_invalid(db, client):
    response = client.post(api_link, {"access_token": "invalid"})
    assert response.status_code == 400


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_api_returns_400_if_user_data_in_token_is_invalid(db, client):
    token = jwt.encode(
        {"username": "jkowalski", "email": "jkowalski@example.com"},
        TEST_SSO_SETTINGS["sso_private_key"],
        algorithm="HS256",
    ).decode("ascii")

    response = client.post(api_link, {"access_token": token})
    assert response.status_code == 400


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_api_creates_user_account_if_user_data_is_valid(db, client):
    token = jwt.encode(
        {"id": 1, "username": "jkowalski", "email": "jkowalski@example.com"},
        TEST_SSO_SETTINGS["sso_private_key"],
        algorithm="HS256",
    ).decode("ascii")

    response = client.post(api_link, {"access_token": token})
    assert response.status_code == 200

    user = User.objects.get(sso_id=1)
    assert user.username == "jkowalski"
    assert user.email == "jkowalski@example.com"


@override_dynamic_settings(**TEST_SSO_SETTINGS)
def test_sso_api_returns_user_id_if_user_data_is_valid(db, client):
    token = jwt.encode(
        {"id": 1, "username": "jkowalski", "email": "jkowalski@example.com"},
        TEST_SSO_SETTINGS["sso_private_key"],
        algorithm="HS256",
    ).decode("ascii")

    response = client.post(api_link, {"access_token": token})

    user = User.objects.get(sso_id=1)
    assert response.json() == {"id": user.pk}
