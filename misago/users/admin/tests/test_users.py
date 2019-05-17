import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ....acl.models import Role
from ....legal.models import Agreement
from ....legal.utils import save_user_agreement_acceptance
from ....test import assert_contains
from ...models import Rank
from ...utils import hash_email

User = get_user_model()


def test_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, reverse("misago:admin:users:index"))


def test_list_renders_with_item(admin_client, users_admin_link, superuser):
    response = admin_client.get(users_admin_link)
    assert_contains(response, superuser.username)


def test_new_user_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:users:new"))
    assert response.status_code == 200


def test_new_user_can_be_created(admin_client):
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
            "staff_level": "0",
        },
    )

    user = User.objects.get_by_email("user@example.com")
    assert user.username == "User"
    assert user.rank == default_rank
    assert authenticated_role in user.roles.all()
    assert user.check_password("pass123")
    assert not user.is_staff
    assert not user.is_superuser


def test_new_user_can_be_created_with_whitespace_around_password(admin_client):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "rank": str(default_rank.pk),
            "roles": str(authenticated_role.pk),
            "email": "user@example.com",
            "new_password": "  pass123  ",
            "staff_level": "0",
        },
    )

    user = User.objects.get_by_email("user@example.com")
    assert user.check_password("  pass123  ")


def test_new_user_creation_fails_because_user_was_not_given_authenticated_role(
    admin_client
):
    default_rank = Rank.objects.get_default()
    guest_role = Role.objects.get(special_role="anonymous")

    admin_client.post(
        reverse("misago:admin:users:new"),
        data={
            "username": "User",
            "rank": str(default_rank.pk),
            "roles": str(guest_role.pk),
            "email": "user@example.com",
            "new_password": "pass123",
            "staff_level": "0",
        },
    )

    with pytest.raises(User.DoesNotExist):
        User.objects.get_by_email("user@example.com")


def test_edit_user_form_renders(admin_client, user):
    response = admin_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200


def test_edit_user_form_renders_for_staff_user(staff_client, user):
    response = staff_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200


def test_edit_staff_form_renders_for_staff_user(staff_client, other_staffuser):
    response = staff_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": other_staffuser.pk})
    )
    assert response.status_code == 200


def test_edit_superuser_form_renders_for_staff_user(staff_client, superuser):
    response = staff_client.get(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk})
    )
    assert response.status_code == 200


def get_default_edit_form_data(user):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")
    data = {
        "username": user.username,
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
        "subscribe_to_started_threads": str(user.subscribe_to_started_threads),
        "subscribe_to_replied_threads": str(user.subscribe_to_replied_threads),
        "is_active": "1",
    }

    if user.is_staff:
        data["is_staff"] = "1"
    if user.is_superuser:
        data["is_superuser"] = "1"

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


def test_admin_editing_their_own_password_is_not_logged_out(admin_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data["new_password"] = "newpassword123"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk}), data=form_data
    )

    user = admin_client.get("/api/auth/")
    assert user.json()["id"] == superuser.id


def test_staff_user_cannot_degrade_superuser_to_staff_user(staff_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data["is_staff"] = "1"
    form_data.pop("is_superuser")

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk}), data=form_data
    )

    superuser.refresh_from_db()
    assert superuser.is_staff
    assert superuser.is_superuser


def test_staff_user_cannot_degrade_superuser_to_regular_user(staff_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data.pop("is_staff")
    form_data.pop("is_superuser")

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk}), data=form_data
    )

    superuser.refresh_from_db()
    assert superuser.is_staff
    assert superuser.is_superuser


def test_staff_user_cannot_promote_other_staff_user_to_superuser(
    staff_client, other_staffuser
):
    form_data = get_default_edit_form_data(other_staffuser)
    form_data["is_staff"] = "1"
    form_data["is_superuser"] = "1"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_staffuser.pk}),
        data=form_data,
    )

    other_staffuser.refresh_from_db()
    assert other_staffuser.is_staff
    assert not other_staffuser.is_superuser


def test_staff_user_cannot_promote_regular_user_to_staff(staff_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_staff"] = "1"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_staff


def test_staff_user_cannot_promote_regular_user_to_superuser(staff_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_superuser"] = "1"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_superuser


def test_staff_user_cannot_promote_themselves_to_superuser(staff_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data["is_superuser"] = "1"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": staffuser.pk}), data=form_data
    )

    staffuser.refresh_from_db()
    assert not staffuser.is_superuser


def test_staff_user_cannot_degrade_themselves_to_regular_user(staff_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data.pop("is_staff")

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": staffuser.pk}), data=form_data
    )

    staffuser.refresh_from_db()
    assert staffuser.is_staff


def test_superuser_cannot_degrade_themselves_to_staff_user(admin_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data.pop("is_superuser")

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk}), data=form_data
    )

    superuser.refresh_from_db()
    assert superuser.is_superuser


def test_superuser_cannot_degrade_themselves_to_regular_user(admin_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data.pop("is_staff")
    form_data.pop("is_superuser")

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk}), data=form_data
    )

    superuser.refresh_from_db()
    assert superuser.is_staff
    assert superuser.is_superuser


def test_superuser_can_degrade_other_superuser_to_staff_user(
    admin_client, other_superuser
):
    form_data = get_default_edit_form_data(other_superuser)
    form_data.pop("is_superuser")

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_superuser.pk}),
        data=form_data,
    )

    other_superuser.refresh_from_db()
    assert other_superuser.is_staff
    assert not other_superuser.is_superuser


def test_superuser_can_degrade_other_superuser_to_regular_user(
    admin_client, other_superuser
):
    form_data = get_default_edit_form_data(other_superuser)
    form_data.pop("is_staff")
    form_data.pop("is_superuser")

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_superuser.pk}),
        data=form_data,
    )

    other_superuser.refresh_from_db()
    assert not other_superuser.is_staff
    assert not other_superuser.is_superuser


def test_superuser_can_promote_to_staff_user_to_superuser(admin_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data["is_superuser"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": staffuser.pk}), data=form_data
    )

    staffuser.refresh_from_db()
    assert staffuser.is_staff
    assert staffuser.is_superuser


def test_superuser_can_promote_to_regular_user_to_staff_user(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_staff"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.is_staff
    assert not user.is_superuser


def test_superuser_can_promote_to_regular_user_to_superuser(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_staff"] = "1"
    form_data["is_superuser"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.is_staff
    assert user.is_superuser


def test_superuser_can_disable_other_superuser_account(admin_client, other_superuser):
    form_data = get_default_edit_form_data(other_superuser)
    form_data["is_active"] = "0"
    form_data["is_active_staff_message"] = "Test message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_superuser.pk}),
        data=form_data,
    )

    other_superuser.refresh_from_db()
    assert not other_superuser.is_active
    assert other_superuser.is_active_staff_message == "Test message"


def test_superuser_can_reactivate_other_superuser_account(
    admin_client, other_superuser
):
    other_superuser.is_active = False
    other_superuser.save()

    form_data = get_default_edit_form_data(other_superuser)
    form_data["is_active"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_superuser.pk}),
        data=form_data,
    )

    other_superuser.refresh_from_db()
    assert other_superuser.is_active


def test_superuser_can_disable_staff_user_account(admin_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data["is_active"] = "0"
    form_data["is_active_staff_message"] = "Test message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": staffuser.pk}), data=form_data
    )

    staffuser.refresh_from_db()
    assert not staffuser.is_active
    assert staffuser.is_active_staff_message == "Test message"


def test_superuser_can_reactivate_staff_user_account(admin_client, staffuser):
    staffuser.is_active = False
    staffuser.save()

    form_data = get_default_edit_form_data(staffuser)
    form_data["is_active"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": staffuser.pk}), data=form_data
    )

    staffuser.refresh_from_db()
    assert staffuser.is_active


def test_superuser_can_disable_regular_user_account(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_active"] = "0"
    form_data["is_active_staff_message"] = "Test message"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_active
    assert user.is_active_staff_message == "Test message"


def test_superuser_can_reactivate_regular_user_account(admin_client, user):
    user.is_active = False
    user.save()

    form_data = get_default_edit_form_data(user)
    form_data["is_active"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.is_active


def test_staff_user_can_disable_regular_user_account(staff_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_active"] = "0"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_active


def test_staff_user_can_reactivate_regular_user_account(staff_client, user):
    user.is_active = False
    user.save()

    form_data = get_default_edit_form_data(user)
    form_data["is_active"] = "1"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert user.is_active


def test_superuser_cant_disable_their_own_account(admin_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data["is_active"] = "0"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk}), data=form_data
    )

    superuser.refresh_from_db()
    assert superuser.is_active


def test_staff_user_cant_disable_their_own_account(staff_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data["is_active"] = "0"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": staffuser.pk}), data=form_data
    )

    staffuser.refresh_from_db()
    assert staffuser.is_active


def test_staff_user_cant_disable_superuser_account(staff_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data["is_active"] = "0"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": superuser.pk}), data=form_data
    )

    superuser.refresh_from_db()
    assert superuser.is_active


def test_staff_user_cant_disable_other_staff_user_account(
    staff_client, other_staffuser
):
    form_data = get_default_edit_form_data(other_staffuser)
    form_data["is_active"] = "0"

    staff_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": other_staffuser.pk}),
        data=form_data,
    )

    other_staffuser.refresh_from_db()
    assert other_staffuser.is_active


def test_user_deleting_their_account_cant_be_reactivated(admin_client, user):
    user.mark_for_delete()

    form_data = get_default_edit_form_data(user)
    form_data["is_active"] = "1"

    admin_client.post(
        reverse("misago:admin:users:edit", kwargs={"pk": user.pk}), data=form_data
    )

    user.refresh_from_db()
    assert not user.is_active


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
