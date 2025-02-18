import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ....acl.models import Role
from ....legal.models import Agreement
from ....legal.utils import save_user_agreement_acceptance
from ....permissions.permissionsid import get_permissions_id
from ....test import assert_contains
from ...models import Rank
from ...utils import hash_email

User = get_user_model()


def test_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, reverse("misago:admin:users:index"))


def test_list_renders_with_item(admin_client, users_admin_link, other_user):
    response = admin_client.get(users_admin_link)
    assert_contains(response, other_user.username)


def test_new_user_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:users:new"))
    assert response.status_code == 200


def test_new_user_can_be_created(admin_client, members_group):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(members_group.id),
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )

    user = User.objects.get_by_email("user@example.com")
    assert user.username == "User"
    assert user.group == members_group
    assert user.groups_ids == [members_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)
    assert user.rank == default_rank
    assert authenticated_role in user.roles.all()
    assert user.check_password("pass123")
    assert not user.is_misago_root


def test_new_user_can_be_created_with_whitespace_around_password(
    admin_client, members_group
):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(members_group.id),
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "  pass123  ",
        },
    )

    user = User.objects.get_by_email("user@example.com")
    assert user.check_password("  pass123  ")


def test_new_user_can_be_created_with_secondary_groups(
    admin_client, moderators_group, members_group, guests_group
):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(members_group.id),
            "secondary_groups": [str(moderators_group.id), str(guests_group.id)],
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )

    user = User.objects.get_by_email("user@example.com")
    assert user.username == "User"
    assert user.group == members_group
    assert user.groups_ids == [moderators_group.id, members_group.id, guests_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)
    assert user.rank == default_rank
    assert authenticated_role in user.roles.all()
    assert user.check_password("pass123")
    assert not user.is_misago_root


def test_root_admin_can_create_user_with_admin_main_group(
    root_admin_client, admins_group
):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    root_admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(admins_group.id),
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )

    user = User.objects.get_by_email("user@example.com")
    assert user.username == "User"
    assert user.group == admins_group
    assert user.groups_ids == [admins_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)
    assert user.rank == default_rank
    assert authenticated_role in user.roles.all()
    assert user.check_password("pass123")
    assert not user.is_misago_root


def test_root_admin_can_create_user_with_admin_secondary_group(
    root_admin_client, admins_group, members_group
):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    root_admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(members_group.id),
            "secondary_groups": [str(admins_group.id)],
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )

    user = User.objects.get_by_email("user@example.com")
    assert user.username == "User"
    assert user.group == members_group
    assert user.groups_ids == [admins_group.id, members_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)
    assert user.rank == default_rank
    assert authenticated_role in user.roles.all()
    assert user.check_password("pass123")
    assert not user.is_misago_root


def test_new_user_creation_fails_because_user_was_not_given_group(
    admin_client,
):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )

    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_email("user@example.com")


def test_new_user_creation_fails_because_admin_user_cant_set_admin_group(
    admin_client, admins_group
):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    response = admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(admins_group.id),
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )
    assert_contains(
        response,
        (
            "You must be a root administrator to set this user&#x27;s "
            "main group to the Administrators."
        ),
    )

    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_email("user@example.com")


def test_new_user_creation_fails_because_admin_user_cant_set_secondary_admin_group(
    admin_client, admins_group, members_group
):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    response = admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(members_group.id),
            "secondary_groups": [str(admins_group.id)],
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )
    assert_contains(
        response,
        (
            "You must be a root administrator to add this user "
            "to the Administrators group."
        ),
    )

    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_email("user@example.com")


def test_new_user_creation_fails_because_user_was_not_given_authenticated_role(
    admin_client, members_group
):
    default_rank = Rank.objects.get_default()
    guest_role = Role.objects.get(special_role="anonymous")

    admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "group": str(members_group.id),
            "rank": str(default_rank.pk),
            "roles": str(guest_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
        },
    )

    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_email("user@example.com")


def test_edit_user_form_renders(admin_client, user):
    response = admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200


def test_edit_user_form_renders_for_root_admin(root_admin_client, user):
    response = root_admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200


def test_edit_admin_form_renders_for_admin_user(admin_client, other_admin):
    response = admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": other_admin.pk})
    )
    assert response.status_code == 200


def test_edit_admin_form_renders_for_root_admin(root_admin_client, other_admin):
    response = root_admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": other_admin.pk})
    )
    assert response.status_code == 200


def test_edit_root_admin_form_renders_for_admin_user(admin_client, root_admin):
    response = admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk})
    )
    assert response.status_code == 200


def test_edit_root_admin_form_renders_for_root_admin(
    root_admin_client, other_root_admin
):
    response = root_admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": other_root_admin.pk})
    )
    assert response.status_code == 200


def get_default_edit_form_data(user):
    data = {
        "username": user.username,
        "group": str(user.group_id),
        "secondary_groups": [
            str(group_id) for group_id in user.groups_ids if group_id != user.group_id
        ],
        "rank": str(user.rank_id),
        "roles": str(user.roles.all()[0].id),
        "email": user.email,
        "new_password": "",
        "signature": user.signature or "",
        "is_signature_locked": str(user.is_signature_locked),
        "is_hiding_presence": str(user.is_hiding_presence),
        "limits_private_thread_invites_to": str(user.limits_private_thread_invites_to),
        "signature_lock_staff_message": str(user.signature_lock_staff_message or ""),
        "signature_lock_user_message": str(user.signature_lock_user_message or ""),
        "watch_started_threads": str(user.watch_started_threads),
        "watch_replied_threads": str(user.watch_replied_threads),
        "watch_new_private_threads_by_followed": str(
            user.watch_new_private_threads_by_followed
        ),
        "watch_new_private_threads_by_other_users": str(
            user.watch_new_private_threads_by_other_users
        ),
        "notify_new_private_threads_by_followed": str(
            user.notify_new_private_threads_by_followed
        ),
        "notify_new_private_threads_by_other_users": str(
            user.notify_new_private_threads_by_other_users
        ),
        "is_active": "1",
    }

    if user.is_misago_root:
        data["is_misago_root"] = "1"

    return data


def test_edit_form_changes_user_username(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["username"] = "NewUsername"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.username == "NewUsername"
    assert user.slug == "newusername"


def test_editing_user_username_creates_entry_in_username_history(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["username"] = "NewUsername"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    assert user.namechanges.exists()


def test_not_editing_user_username_doesnt_create_entry_in_username_history(
    admin_client, user
):
    form_data = get_default_edit_form_data(user)

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    assert not user.namechanges.exists()


def test_edit_form_changes_user_email(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["email"] = "edited@example.com"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.email == "edited@example.com"
    assert user.email_hash == hash_email("edited@example.com")


def test_admin_can_change_own_email(admin_client, admin):
    form_data = get_default_edit_form_data(admin)
    form_data["email"] = "edited@example.com"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}), data=form_data
    )

    admin.refresh_from_db()
    assert admin.email == "edited@example.com"
    assert admin.email_hash == hash_email("edited@example.com")


def test_admin_cant_change_other_admin_email(admin_client, other_admin):
    form_data = get_default_edit_form_data(other_admin)
    form_data["email"] = "edited@example.com"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_admin.pk}),
        data=form_data,
    )

    other_admin.refresh_from_db()
    assert other_admin.email == "otheradmin@example.com"
    assert other_admin.email_hash == hash_email("otheradmin@example.com")


def test_admin_cant_change_root_admin_email(admin_client, root_admin):
    form_data = get_default_edit_form_data(root_admin)
    form_data["email"] = "edited@example.com"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk}), data=form_data
    )

    root_admin.refresh_from_db()
    assert root_admin.email == "rootadmin@example.com"
    assert root_admin.email_hash == hash_email("rootadmin@example.com")


def test_root_admin_can_change_admin_email(root_admin_client, admin):
    form_data = get_default_edit_form_data(admin)
    form_data["email"] = "edited@example.com"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}), data=form_data
    )

    admin.refresh_from_db()
    assert admin.email == "edited@example.com"
    assert admin.email_hash == hash_email("edited@example.com")


def test_root_admin_can_change_other_root_admin_email(
    root_admin_client, other_root_admin
):
    form_data = get_default_edit_form_data(other_root_admin)
    form_data["email"] = "edited@example.com"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_root_admin.pk}),
        data=form_data,
    )

    other_root_admin.refresh_from_db()
    assert other_root_admin.email == "edited@example.com"
    assert other_root_admin.email_hash == hash_email("edited@example.com")


def test_edit_form_doesnt_remove_current_user_password_if_new_password_is_omitted(
    admin_client, user, user_password
):
    form_data = get_default_edit_form_data(user)

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.check_password(user_password)


def test_edit_form_displays_message_for_user_with_unusable_password(
    admin_client, user, user_password
):
    user.set_password(None)
    user.save()

    response = admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk})
    )

    assert_contains(response, "alert-has-unusable-password")


def test_edit_form_doesnt_set_password_for_user_with_unusable_password_if_none_is_given(
    admin_client, user, user_password
):
    user.set_password(None)
    user.save()

    form_data = get_default_edit_form_data(user)

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.has_usable_password()


def test_edit_form_sets_password_for_user_with_unusable_password(
    admin_client, user, user_password
):
    user.set_password(None)
    user.save()

    form_data = get_default_edit_form_data(user)
    form_data["new_password"] = user_password

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.check_password(user_password)


def test_edit_form_changes_user_password(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["new_password"] = "newpassword123"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.check_password("newpassword123")


def test_edit_form_preserves_whitespace_in_new_user_password(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["new_password"] = "  newpassword123  "

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.check_password("  newpassword123  ")


def test_root_admin_can_change_own_password(root_admin_client, root_admin):
    form_data = get_default_edit_form_data(root_admin)
    form_data["new_password"] = "newpassword123"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk}), data=form_data
    )

    root_admin.refresh_from_db()
    assert root_admin.check_password("newpassword123")


def test_root_admin_can_change_other_root_admin_password(
    root_admin_client, other_root_admin
):
    form_data = get_default_edit_form_data(other_root_admin)
    form_data["new_password"] = "newpassword123"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_root_admin.pk}),
        data=form_data,
    )

    other_root_admin.refresh_from_db()
    assert other_root_admin.check_password("newpassword123")


def test_root_admin_can_change_admin_password(root_admin_client, admin):
    form_data = get_default_edit_form_data(admin)
    form_data["new_password"] = "newpassword123"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}), data=form_data
    )

    admin.refresh_from_db()
    assert admin.check_password("newpassword123")


def test_admin_can_change_own_password(admin_client, admin):
    form_data = get_default_edit_form_data(admin)
    form_data["new_password"] = "newpassword123"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}), data=form_data
    )

    admin.refresh_from_db()
    assert admin.check_password("newpassword123")


def test_admin_cant_change_root_admin_password(
    admin_client, other_root_admin, user_password
):
    form_data = get_default_edit_form_data(other_root_admin)
    form_data["new_password"] = "newpassword123"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_root_admin.pk}),
        data=form_data,
    )

    other_root_admin.refresh_from_db()
    assert other_root_admin.check_password(user_password)


def test_admin_can_change_other_admin_password(
    admin_client, other_admin, user_password
):
    form_data = get_default_edit_form_data(other_admin)
    form_data["new_password"] = "newpassword123"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_admin.pk}),
        data=form_data,
    )

    other_admin.refresh_from_db()
    assert other_admin.check_password(user_password)


def test_admin_editing_their_own_password_is_not_logged_out(admin_client, admin):
    form_data = get_default_edit_form_data(admin)
    form_data["new_password"] = "newpassword123"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}), data=form_data
    )

    user = admin_client.get("/api/auth/")
    assert user.json()["id"] == admin.id


def test_root_admin_can_change_other_user_main_group_to_admin(
    root_admin_client, user, admins_group
):
    form_data = get_default_edit_form_data(user)
    form_data["group"] = str(admins_group.id)

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.group_id == admins_group.id
    assert user.groups_ids == [admins_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_root_admin_can_change_other_user_secondary_group_to_admin(
    root_admin_client, user, admins_group, members_group
):
    form_data = get_default_edit_form_data(user)
    form_data["secondary_groups"] = [str(admins_group.id)]

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.group_id == members_group.id
    assert user.groups_ids == [admins_group.id, members_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_admin_cant_change_other_user_main_group_to_admin(
    admin_client, user, admins_group, members_group
):
    form_data = get_default_edit_form_data(user)
    form_data["group"] = str(admins_group.id)

    response = admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )
    assert_contains(
        response,
        (
            "You must be a root administrator "
            "to change this user&#x27;s main group to the Administrators"
        ),
    )

    user.refresh_from_db()
    assert user.group_id == members_group.id
    assert user.groups_ids == [members_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_admin_cant_change_other_user_secondary_group_to_admin(
    admin_client, user, admins_group, members_group
):
    form_data = get_default_edit_form_data(user)
    form_data["secondary_groups"] = [str(admins_group.id)]

    response = admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )
    assert_contains(
        response,
        (
            "You must be a root administrator to add this user "
            "to the Administrators group."
        ),
    )

    user.refresh_from_db()
    assert user.group_id == members_group.id
    assert user.groups_ids == [members_group.id]
    assert user.permissions_id == get_permissions_id(user.groups_ids)


def test_root_admin_can_change_other_user_main_group_from_admin(
    root_admin_client, admin, members_group
):
    form_data = get_default_edit_form_data(admin)
    form_data["group"] = str(members_group.id)

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}), data=form_data
    )

    admin.refresh_from_db()
    assert admin.group_id == members_group.id
    assert admin.groups_ids == [members_group.id]
    assert admin.permissions_id == get_permissions_id(admin.groups_ids)


def test_root_admin_can_change_other_user_secondary_group_from_admin(
    root_admin_client, secondary_admin, members_group
):
    form_data = get_default_edit_form_data(secondary_admin)
    form_data.pop("secondary_groups")

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": secondary_admin.pk}),
        data=form_data,
    )

    secondary_admin.refresh_from_db()
    assert secondary_admin.group_id == members_group.id
    assert secondary_admin.groups_ids == [members_group.id]
    assert secondary_admin.permissions_id == get_permissions_id(
        secondary_admin.groups_ids
    )


def test_admin_cant_change_other_user_main_group_from_admin(
    admin_client, other_admin, admins_group, members_group
):
    form_data = get_default_edit_form_data(other_admin)
    form_data["group"] = str(members_group.id)

    response = admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_admin.pk}),
        data=form_data,
    )
    assert_contains(
        response,
        (
            "You must be a root administrator to change this user&#x27;s "
            "main group from the Administrators."
        ),
    )

    other_admin.refresh_from_db()
    assert other_admin.group_id == admins_group.id
    assert other_admin.groups_ids == [admins_group.id]
    assert other_admin.permissions_id == get_permissions_id(other_admin.groups_ids)


def test_admin_cant_change_other_user_secondary_group_from_admin(
    admin_client, secondary_admin, admins_group, members_group
):
    form_data = get_default_edit_form_data(secondary_admin)
    form_data.pop("secondary_groups")

    response = admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": secondary_admin.pk}),
        data=form_data,
    )
    assert_contains(
        response,
        (
            "You must be a root administrator to remove this user "
            "from the Administrators group."
        ),
    )

    secondary_admin.refresh_from_db()
    assert secondary_admin.group_id == members_group.id
    assert secondary_admin.groups_ids == [admins_group.id, members_group.id]
    assert secondary_admin.permissions_id == get_permissions_id(
        secondary_admin.groups_ids
    )


def test_admin_can_change_other_admin_main_group(
    admin_client, secondary_admin, admins_group, moderators_group
):
    form_data = get_default_edit_form_data(secondary_admin)
    form_data["group"] = str(moderators_group.id)

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": secondary_admin.pk}),
        data=form_data,
    )

    secondary_admin.refresh_from_db()
    assert secondary_admin.group_id == moderators_group.id
    assert secondary_admin.groups_ids == [admins_group.id, moderators_group.id]
    assert secondary_admin.permissions_id == get_permissions_id(
        secondary_admin.groups_ids
    )


def test_admin_can_add_other_admin_secondary_group(
    admin_client, secondary_admin, admins_group, moderators_group, members_group
):
    form_data = get_default_edit_form_data(secondary_admin)
    form_data["secondary_groups"] = [str(admins_group.id), str(moderators_group.id)]

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": secondary_admin.pk}),
        data=form_data,
    )

    secondary_admin.refresh_from_db()
    assert secondary_admin.group_id == members_group.id
    assert secondary_admin.groups_ids == [
        admins_group.id,
        moderators_group.id,
        members_group.id,
    ]
    assert secondary_admin.permissions_id == get_permissions_id(
        secondary_admin.groups_ids
    )


def test_admin_can_remove_other_admin_secondary_group(
    admin_client, secondary_admin, admins_group, moderators_group, members_group
):
    secondary_admin.set_groups(members_group, [admins_group, moderators_group])
    secondary_admin.save()

    form_data = get_default_edit_form_data(secondary_admin)
    form_data["secondary_groups"] = [str(admins_group.id)]

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": secondary_admin.pk}),
        data=form_data,
    )

    secondary_admin.refresh_from_db()
    assert secondary_admin.group_id == members_group.id
    assert secondary_admin.groups_ids == [admins_group.id, members_group.id]
    assert secondary_admin.permissions_id == get_permissions_id(
        secondary_admin.groups_ids
    )


def test_root_admin_can_promote_other_user_to_root(root_admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_misago_root"] = "1"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.is_misago_root


def test_root_admin_can_remove_other_user_root_status(
    root_admin_client, other_root_admin
):
    form_data = get_default_edit_form_data(other_root_admin)
    form_data.pop("is_misago_root")

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_root_admin.pk}),
        data=form_data,
    )

    other_root_admin.refresh_from_db()
    assert not other_root_admin.is_misago_root


def test_root_admin_cannot_remove_their_own_root_status(root_admin_client, root_admin):
    form_data = get_default_edit_form_data(root_admin)
    form_data.pop("is_misago_root")

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk}), data=form_data
    )

    root_admin.refresh_from_db()
    assert root_admin.is_misago_root


def test_admin_cant_promote_other_user_to_root_status(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_misago_root"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_misago_root


def test_admin_cant_remove_other_user_root_status(admin_client, root_admin):
    form_data = get_default_edit_form_data(root_admin)
    form_data.pop("is_misago_root")

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk}), data=form_data
    )

    root_admin.refresh_from_db()
    assert root_admin.is_misago_root


def test_admin_can_activate_user_account(admin_client, inactive_user):
    form_data = get_default_edit_form_data(inactive_user)
    form_data["is_active"] = "1"
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": inactive_user.pk}),
        data=form_data,
    )

    inactive_user.refresh_from_db()
    assert inactive_user.is_active
    assert inactive_user.is_active_staff_message == "Message"


def test_root_admin_can_activate_admin_account(root_admin_client, admin):
    admin.is_active = False
    admin.is_active_staff_message = None
    admin.save()

    form_data = get_default_edit_form_data(admin)
    form_data["is_active"] = "1"
    form_data["is_active_staff_message"] = "Message"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}),
        data=form_data,
    )

    admin.refresh_from_db()
    assert admin.is_active
    assert admin.is_active_staff_message == "Message"


def test_root_admin_can_activate_other_root_admin_account(
    root_admin_client, other_root_admin
):
    other_root_admin.is_active = False
    other_root_admin.is_active_staff_message = None
    other_root_admin.save()

    form_data = get_default_edit_form_data(other_root_admin)
    form_data["is_active"] = "1"
    form_data["is_active_staff_message"] = "Message"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_root_admin.pk}),
        data=form_data,
    )

    other_root_admin.refresh_from_db()
    assert other_root_admin.is_active
    assert other_root_admin.is_active_staff_message == "Message"


def test_admin_cant_activate_other_admin_account(admin_client, other_admin):
    other_admin.is_active = False
    other_admin.is_active_staff_message = None
    other_admin.save()

    form_data = get_default_edit_form_data(other_admin)
    form_data["is_active"] = "1"
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_admin.pk}),
        data=form_data,
    )

    other_admin.refresh_from_db()
    assert not other_admin.is_active
    assert not other_admin.is_active_staff_message


def test_admin_cant_activate_root_admin_account(admin_client, root_admin):
    root_admin.is_active = False
    root_admin.is_active_staff_message = None
    root_admin.save()

    form_data = get_default_edit_form_data(root_admin)
    form_data["is_active"] = "1"
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk}),
        data=form_data,
    )

    root_admin.refresh_from_db()
    assert not root_admin.is_active
    assert not root_admin.is_active_staff_message


def test_admin_can_deactivate_user_account(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data.pop("is_active")
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    user.refresh_from_db()
    assert not user.is_active
    assert user.is_active_staff_message == "Message"


def test_root_admin_can_deactivate_admin_account(root_admin_client, admin):
    form_data = get_default_edit_form_data(admin)
    form_data.pop("is_active")
    form_data["is_active_staff_message"] = "Message"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}),
        data=form_data,
    )

    admin.refresh_from_db()
    assert not admin.is_active
    assert admin.is_active_staff_message == "Message"


def test_root_admin_can_deactivate_other_root_admin_account(
    root_admin_client, other_root_admin
):
    form_data = get_default_edit_form_data(other_root_admin)
    form_data.pop("is_active")
    form_data["is_active_staff_message"] = "Message"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_root_admin.pk}),
        data=form_data,
    )

    other_root_admin.refresh_from_db()
    assert not other_root_admin.is_active
    assert other_root_admin.is_active_staff_message == "Message"


def test_admin_cant_deactivate_other_admin_account(admin_client, other_admin):
    form_data = get_default_edit_form_data(other_admin)
    form_data.pop("is_active")
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_admin.pk}),
        data=form_data,
    )

    other_admin.refresh_from_db()
    assert other_admin.is_active
    assert not other_admin.is_active_staff_message


def test_admin_cant_deactivate_root_admin_account(admin_client, root_admin):
    form_data = get_default_edit_form_data(root_admin)
    form_data.pop("is_active")
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk}),
        data=form_data,
    )

    root_admin.refresh_from_db()
    assert root_admin.is_active
    assert not root_admin.is_active_staff_message


def test_admin_cant_deactivate_own_account(admin_client, admin):
    form_data = get_default_edit_form_data(admin)
    form_data.pop("is_active")
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": admin.pk}),
        data=form_data,
    )

    admin.refresh_from_db()
    assert admin.is_active
    assert not admin.is_active_staff_message


def test_root_admin_cant_deactivate_own_account(root_admin_client, root_admin):
    form_data = get_default_edit_form_data(root_admin)
    form_data.pop("is_active")
    form_data["is_active_staff_message"] = "Message"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": root_admin.pk}),
        data=form_data,
    )

    root_admin.refresh_from_db()
    assert root_admin.is_active
    assert not root_admin.is_active_staff_message


def test_admin_cant_activate_user_deleting_their_account(admin_client, user):
    user.mark_for_delete()

    form_data = get_default_edit_form_data(user)
    form_data["is_active"] = "1"
    form_data["is_active_staff_message"] = "Message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_active
    assert not user.is_active_staff_message


def test_root_admin_cant_activate_user_deleting_their_account(root_admin_client, user):
    user.mark_for_delete()

    form_data = get_default_edit_form_data(user)
    form_data["is_active"] = "1"
    form_data["is_active_staff_message"] = "Message"

    root_admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_active
    assert not user.is_active_staff_message


def test_user_agreements_are_displayed_on_edit_form(admin_client, user):
    agreement = Agreement.objects.create(
        type=Agreement.TYPE_TOS,
        title="Test agreement!",
        text="Lorem ipsum!",
        is_active=True,
    )

    save_user_agreement_acceptance(user, agreement, commit=True)

    response = admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk})
    )
    assert_contains(response, agreement.title)
