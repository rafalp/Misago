from django.urls import reverse


def test_healtcheck_returns_200_response(db, user_client):
    response = user_client.get(reverse("misago:healthcheck"))
    assert response.status_code == 200
