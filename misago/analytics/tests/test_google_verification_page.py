from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains


@override_dynamic_settings(google_site_verification=None)
def test_verification_page_returns_404_if_verification_token_is_not_set(db, client):
    response = client.get("/googlet0k3n.html")
    assert response.status_code == 404


@override_dynamic_settings(google_site_verification="t0k3n")
def test_verification_page_returns_404_if_verification_token_is_invalid(db, client):
    response = client.get("/googleinv4l1d.html")
    assert response.status_code == 404


@override_dynamic_settings(google_site_verification="t0k3n")
def test_verification_page_returns_google_verification_token(db, client):
    response = client.get("/googlet0k3n.html")
    assert response.status_code == 200
    assert_contains(response, f"google-site-verification: googlet0k3n.html")
