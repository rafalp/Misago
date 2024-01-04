import pytest
from django.urls import reverse

from ...cache.enums import CacheName
from ...cache.test import assert_invalidates_cache
from ...permissions.models import Moderator
from ...test import assert_has_error_message


def test_group_moderator_is_deleted(admin_client, custom_group):
    moderator = Moderator.objects.create(group=custom_group)

    response = admin_client.post(
        reverse("misago:admin:moderators:delete", kwargs={"pk": moderator.id})
    )
    assert response.status_code == 302

    with pytest.raises(Moderator.DoesNotExist):
        moderator.refresh_from_db()


def test_user_moderator_is_deleted(admin_client, other_user):
    moderator = Moderator.objects.create(user=other_user)

    response = admin_client.post(
        reverse("misago:admin:moderators:delete", kwargs={"pk": moderator.id})
    )
    assert response.status_code == 302

    with pytest.raises(Moderator.DoesNotExist):
        moderator.refresh_from_db()


def test_deleting_moderator_invalidates_moderators_cache(admin_client, custom_group):
    moderator = Moderator.objects.create(group=custom_group)

    with assert_invalidates_cache(CacheName.MODERATORS):
        admin_client.post(
            reverse("misago:admin:moderators:delete", kwargs={"pk": moderator.id})
        )


def test_protected_moderator_cant_be_deleted(admin_client, admins_group):
    moderator = Moderator.objects.get(group=admins_group)

    response = admin_client.post(
        reverse("misago:admin:moderators:delete", kwargs={"pk": moderator.id})
    )
    assert_has_error_message(
        response,
        'Can\'t remove "Administrators" moderator permissions because they are protected.',
    )


def test_non_existing_moderator_cant_be_deleted(admin_client):
    response = admin_client.post(
        reverse("misago:admin:moderators:delete", kwargs={"pk": 404})
    )
    assert_has_error_message(response, "Requested moderator does not exist.")
