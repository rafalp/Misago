from django.urls import reverse

from ...test import assert_has_error_message


def test_group_members_shortcut_handles_non_existing_group(admin_client):
    response = admin_client.get(
        reverse("misago:admin:groups:members", kwargs={"pk": 404})
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested group does not exist.")


def test_group_members_shortcut_redirects_to_users(admin_client, admins_group):
    response = admin_client.get(
        reverse("misago:admin:groups:members", kwargs={"pk": admins_group.pk})
    )
    assert response.status_code == 302

    users_list = reverse("misago:admin:users:index")
    assert response["location"] == f"{users_list}?group={admins_group.id}"


def test_group_main_members_shortcut_handles_non_existing_group(admin_client):
    response = admin_client.get(
        reverse("misago:admin:groups:members-main", kwargs={"pk": 404})
    )
    assert response.status_code == 302
    assert_has_error_message(response, "Requested group does not exist.")


def test_group_main_members_shortcut_redirects_to_users(admin_client, admins_group):
    response = admin_client.get(
        reverse("misago:admin:groups:members-main", kwargs={"pk": admins_group.pk})
    )
    assert response.status_code == 302

    users_list = reverse("misago:admin:users:index")
    assert response["location"] == f"{users_list}?main_group={admins_group.id}"
