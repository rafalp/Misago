import json

from django.urls import reverse

from ..bans import ban_ip, ban_user
from ..models import Ban


def test_user_middleware_sets_authenticated_user(user_client, user):
    response = user_client.get(reverse("misago:api:auth"))
    assert json.loads(response.content)["id"] == user.id


def test_user_middleware_doesnt_pass_banned_user(user_client, user):
    ban_user(user)

    response = user_client.get(reverse("misago:api:auth"))
    assert json.loads(response.content)["id"] is None


def test_user_middleware_passes_banned_admin_user(admin_client, admin):
    ban_user(admin)

    response = admin_client.get(reverse("misago:api:auth"))
    assert json.loads(response.content)["id"] == admin.id


def test_user_middleware_doesnt_pass_banned_ip_user(user_client):
    ban_ip("127.0.0.1")

    response = user_client.get(reverse("misago:api:auth"))
    assert json.loads(response.content)["id"] is None


def test_user_middleware_passes_banned_ip_admin_user(admin_client, admin):
    ban_ip("127.0.0.1")

    response = admin_client.get(reverse("misago:api:auth"))
    assert json.loads(response.content)["id"] == admin.id


def test_user_middleware_skips_registration_only_bans(user_client, user):
    Ban.objects.create(
        check_type=Ban.USERNAME,
        banned_value="%s*" % user.username[:3],
        registration_only=True,
    )

    response = user_client.get(reverse("misago:api:auth"))
    assert json.loads(response.content)["id"] == user.id
