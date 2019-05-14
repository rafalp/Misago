import pytest
from django.urls import reverse

from ....admin.test import AdminTestCase
from ....cache.test import assert_invalidates_cache
from ....test import assert_contains
from ... import ACL_CACHE
from ...models import Role
from ..test import mock_role_form_data

admin_link = reverse("misago:admin:permissions:index")


def create_form_data(data_dict):
    return mock_role_form_data(Role(), data_dict)


def test_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, admin_link)


def test_list_renders(admin_client):
    response = admin_client.get(admin_link)
    assert response.status_code == 200


def test_new_role_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:permissions:new"))
    assert response.status_code == 200


def test_new_role_can_be_created(admin_client):
    response = admin_client.post(
        reverse("misago:admin:permissions:new"),
        data=create_form_data({"name": "Test Role"}),
    )

    Role.objects.get(name="Test Role")


@pytest.fixture
def role(db):
    return Role.objects.create(name="Test Role")


def test_edit_role_form_renders(admin_client, role):
    response = admin_client.get(
        reverse("misago:admin:permissions:edit", kwargs={"pk": role.pk})
    )
    assert response.status_code == 200


def test_role_can_be_edited(admin_client, role):
    response = admin_client.post(
        reverse("misago:admin:permissions:edit", kwargs={"pk": role.pk}),
        data=create_form_data({"name": "Edited Role"}),
    )

    role.refresh_from_db()
    assert role.name == "Edited Role"


def test_editing_role_invalidates_acl_cache(admin_client, role):
    with assert_invalidates_cache(ACL_CACHE):
        admin_client.post(
            reverse("misago:admin:permissions:edit", kwargs={"pk": role.pk}),
            data=create_form_data({"name": "Role"}),
        )


def test_role_can_be_deleted(admin_client, role):
    admin_client.post(
        reverse("misago:admin:permissions:delete", kwargs={"pk": role.pk})
    )

    with pytest.raises(Role.DoesNotExist):
        role.refresh_from_db()


def test_special_role_cant_be_deleted(admin_client, role):
    role.special_role = "Test"
    role.save()

    admin_client.post(
        reverse("misago:admin:permissions:delete", kwargs={"pk": role.pk})
    )

    role.refresh_from_db()


def test_deleting_role_invalidates_acl_cache(admin_client, role):
    with assert_invalidates_cache(ACL_CACHE):
        admin_client.post(
            reverse("misago:admin:permissions:delete", kwargs={"pk": role.pk})
        )


def test_users_with_role_view_redirects_to_admin_users_list(admin_client, role):
    response = admin_client.get(
        reverse("misago:admin:permissions:users", kwargs={"pk": role.pk})
    )
    assert response.status_code == 302
    assert reverse("misago:admin:users:index") in response["location"]
