from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains


@override_dynamic_settings(google_site_verification=None)
def test_verification_page_returns_404_if_verification_token_is_not_set(db, client):
    verification_link = reverse(
        "misago:google-site-verification", kwargs={"token": "t0k3n"}
    )
    response = client.get(verification_link)
    assert response.status_code == 404


@override_dynamic_settings(google_site_verification="t0k3n")
def test_verification_page_returns_404_if_verification_token_is_invalid(db, client):
    verification_link = reverse(
        "misago:google-site-verification", kwargs={"token": "inv4l1d"}
    )
    response = client.get(verification_link)
    assert response.status_code == 404


@override_dynamic_settings(google_site_verification="t0k3n")
def test_verification_page_returns_200_if_verification_token_is_correct(db, client):
    verification_link = reverse(
        "misago:google-site-verification", kwargs={"token": "t0k3n"}
    )
    response = client.get(verification_link)
    assert response.status_code == 200


@override_dynamic_settings(google_site_verification="t0k3n")
def test_verification_page_contains_token(db, client):
    verification_link = reverse(
        "misago:google-site-verification", kwargs={"token": "t0k3n"}
    )
    response = client.get(verification_link)
    assert_contains(response, "googlet0k3n.html")
