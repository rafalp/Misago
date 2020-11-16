from django.urls import reverse


def test_view_has_no_showstoppers(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert response.status_code == 200
