from django.urls import reverse


def test_captcha_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:captcha:index"))
    assert response.status_code == 200


def test_user_settings_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:settings:users:index"))
    assert response.status_code == 200
