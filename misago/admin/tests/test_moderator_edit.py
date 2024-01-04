from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.models import Moderator
from ...test import assert_contains, assert_has_error_message


def test_moderator_edit_group_form_renders(admin_client, custom_group):
    moderator = Moderator.objects.create(group=custom_group)

    response = admin_client.get(
        reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.pk}),
    )
    assert_contains(response, custom_group.name)


def test_moderator_edit_user_form_renders(admin_client, other_user):
    moderator = Moderator.objects.create(user=other_user)

    response = admin_client.get(
        reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.pk}),
    )
    assert_contains(response, other_user.username)


def test_moderator_edit_group_form_updates_moderator(admin_client, custom_group):
    moderator = Moderator.objects.create(group=custom_group, is_global=True)

    response = admin_client.post(
        reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.pk}),
        {"is_global": "0"},
    )
    assert response.status_code == 302

    moderator.refresh_from_db()
    assert not moderator.is_global


def test_moderator_edit_user_form_updates_moderator(admin_client, other_user):
    moderator = Moderator.objects.create(user=other_user, is_global=True)
    assert moderator.is_global

    response = admin_client.post(
        reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.pk}),
        {"is_global": "0"},
    )
    assert response.status_code == 302

    moderator.refresh_from_db()
    assert not moderator.is_global


def test_moderator_edit_group_form_invalidates_moderators_cache(
    admin_client, custom_group
):
    moderator = Moderator.objects.create(group=custom_group)

    with assert_invalidates_cache(CacheName.MODERATORS):
        admin_client.post(
            reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.pk}),
            {"is_global": "0"},
        )


def test_moderator_edit_user_form_invalidates_moderators_cache(
    admin_client, other_user
):
    moderator = Moderator.objects.create(user=other_user)

    with assert_invalidates_cache(CacheName.MODERATORS):
        admin_client.post(
            reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.pk}),
            {"is_global": "0"},
        )


def test_moderator_edit_handles_non_existing_moderator(admin_client):
    response = admin_client.get(
        reverse("misago:admin:moderators:edit", kwargs={"pk": 404}),
    )
    assert_has_error_message(response, "Requested moderator does not exist.")


def test_moderator_edit_handles_non_protected_moderator(admin_client, admins_group):
    moderator = Moderator.objects.get(group=admins_group)

    response = admin_client.get(
        reverse("misago:admin:moderators:edit", kwargs={"pk": moderator.id}),
    )
    assert_has_error_message(
        response,
        'Can\'t change "Administrators" moderator permissions because they are protected.',
    )
