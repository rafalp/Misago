from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.models import Moderator
from ...test import assert_contains, assert_has_error_message


def test_moderator_new_group_form_is_rendered(admin_client, custom_group):
    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-group",
            kwargs={"group": custom_group.pk},
        )
    )
    assert_contains(response, custom_group.name)


def test_moderator_new_user_form_is_rendered(admin_client, other_user):
    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-user",
            kwargs={"user": other_user.pk},
        )
    )
    assert_contains(response, other_user.username)


def test_moderator_new_group_form_creates_moderator(admin_client, custom_group):
    response = admin_client.post(
        reverse(
            "misago:admin:moderators:new-group",
            kwargs={"group": custom_group.pk},
        ),
        {"is_global": True},
    )
    assert response.status_code == 302

    Moderator.objects.get(group=custom_group, is_global=True)


def test_moderator_new_user_form_creates_moderator(admin_client, other_user):
    response = admin_client.post(
        reverse(
            "misago:admin:moderators:new-user",
            kwargs={"user": other_user.pk},
        ),
        {"is_global": True},
    )
    assert response.status_code == 302

    Moderator.objects.get(user=other_user, is_global=True)


def test_moderator_new_user_form_invalidates_moderator_cache(admin_client, other_user):
    with assert_invalidates_cache(CacheName.MODERATORS):
        admin_client.post(
            reverse(
                "misago:admin:moderators:new-user",
                kwargs={"user": other_user.pk},
            ),
            {"is_global": True},
        )


def test_moderator_new_group_form_handles_non_existing_group(admin_client):
    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-group",
            kwargs={"group": 404},
        )
    )
    assert_has_error_message(response, "Requested user or group does not exist.")


def test_moderator_new_user_form_handles_non_existing_user(admin_client, admin):
    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-user",
            kwargs={"user": admin.id + 404},
        )
    )
    assert_has_error_message(response, "Requested user or group does not exist.")


def test_moderator_new_group_form_redirects_to_existing_moderator(
    admin_client, custom_group
):
    moderator = Moderator.objects.create(group=custom_group)

    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-group",
            kwargs={"group": custom_group.pk},
        )
    )
    assert response.status_code == 302
    assert response.headers["location"].endswith(
        reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.id})
    )


def test_moderator_new_user_form_redirects_to_existing_moderator(
    admin_client, other_user
):
    moderator = Moderator.objects.create(user=other_user)

    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-user",
            kwargs={"user": other_user.pk},
        )
    )
    assert response.status_code == 302
    assert response.headers["location"].endswith(
        reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.id})
    )


def test_moderator_new_group_form_displays_error_if_group_is_default(
    admin_client, custom_group
):
    custom_group.is_default = True
    custom_group.save()

    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-group",
            kwargs={"group": custom_group.pk},
        )
    )
    assert_has_error_message(
        response,
        "Can't grant \"Custom Group\" moderator permissions because it's the default group.",
    )


def test_moderator_new_group_form_displays_error_if_group_is_protected(
    admin_client, guests_group
):
    response = admin_client.get(
        reverse(
            "misago:admin:moderators:new-group",
            kwargs={"group": guests_group.pk},
        )
    )
    assert_has_error_message(
        response,
        "Can't grant \"Guests\" moderator permissions because it's protected group.",
    )
