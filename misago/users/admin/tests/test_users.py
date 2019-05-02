import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

from ....acl.models import Role
from ....admin.test import AdminTestCase
from ....categories.models import Category
from ....legal.models import Agreement
from ....legal.utils import save_user_agreement_acceptance
from ....test import assert_contains
from ....threads.test import post_thread, reply_thread
from ...datadownloads import request_user_data_download
from ...models import Ban, DataDownload, Rank
from ...test import create_test_user
from ...utils import hash_email

User = get_user_model()


def test_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, reverse("misago:admin:users:accounts:index"))


def test_list_renders_with_item(admin_client, users_admin_link, superuser):
    response = admin_client.get(users_admin_link)
    assert_contains(response, superuser.username)


def test_new_user_form_renders(admin_client):
    response = admin_client.get(reverse("misago:admin:users:accounts:new"))
    assert response.status_code == 200


def test_new_user_can_be_created(admin_client):
    default_rank = Rank.objects.get_default()
    authenticated_role = Role.objects.get(special_role="authenticated")

    admin_client.post(
        reverse("misago:admin:users:accounts:new"),
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
        reverse("misago:admin:users:accounts:new"),
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
        reverse("misago:admin:users:accounts:new"),
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
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200


def test_edit_user_form_renders_for_staff_user(staff_client, user):
    response = staff_client.get(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk})
    )
    assert response.status_code == 200


def test_edit_staff_form_renders_for_staff_user(staff_client, other_staffuser):
    response = staff_client.get(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": other_staffuser.pk})
    )
    assert response.status_code == 200


def test_edit_superuser_form_renders_for_staff_user(staff_client, superuser):
    response = staff_client.get(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": superuser.pk})
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
        "signature": user.signature,
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

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    user.refresh_from_db()
    assert user.username == "NewUsername"
    assert user.slug == "newusername"


def test_editing_user_username_creates_entry_in_username_history(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["username"] = "NewUsername"

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    assert user.namechanges.exists()


def test_edit_form_changes_user_email(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["email"] = "edited@example.com"

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    user.refresh_from_db()
    assert user.email == "edited@example.com"
    assert user.email_hash == hash_email("edited@example.com")


def test_staff_user_cannot_degrade_superuser_to_staff_user(staff_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data["is_staff"] = "1"
    form_data.pop("is_superuser")

    response = staff_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": superuser.pk}),
        data=form_data,
    )

    superuser.refresh_from_db()
    assert superuser.is_staff
    assert superuser.is_superuser


def test_staff_user_cannot_degrade_superuser_to_regular_user(staff_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data.pop("is_staff")
    form_data.pop("is_superuser")

    response = staff_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": superuser.pk}),
        data=form_data,
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

    response = staff_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": other_staffuser.pk}),
        data=form_data,
    )

    other_staffuser.refresh_from_db()
    assert other_staffuser.is_staff
    assert not other_staffuser.is_superuser


def test_staff_user_cannot_promote_regular_user_to_staff(staff_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_staff"] = "1"

    response = staff_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    user.refresh_from_db()
    assert not user.is_staff


def test_staff_user_cannot_promote_regular_user_to_superuser(staff_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_superuser"] = "1"

    response = staff_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    user.refresh_from_db()
    assert not user.is_superuser


def test_staff_user_cannot_promote_themselves_to_superuser(staff_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data["is_superuser"] = "1"

    response = staff_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": staffuser.pk}),
        data=form_data,
    )

    staffuser.refresh_from_db()
    assert not staffuser.is_superuser


def test_staff_user_cannot_degrade_themselves_to_regular_user(staff_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data.pop("is_staff")

    response = staff_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": staffuser.pk}),
        data=form_data,
    )

    staffuser.refresh_from_db()
    assert staffuser.is_staff


def test_superuser_cannot_degrade_themselves_to_staff_user(admin_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data.pop("is_superuser")

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": superuser.pk}),
        data=form_data,
    )

    superuser.refresh_from_db()
    assert superuser.is_superuser


def test_superuser_cannot_degrade_themselves_to_regular_user(admin_client, superuser):
    form_data = get_default_edit_form_data(superuser)
    form_data.pop("is_staff")
    form_data.pop("is_superuser")

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": superuser.pk}),
        data=form_data,
    )

    superuser.refresh_from_db()
    assert superuser.is_staff
    assert superuser.is_superuser


def test_superuser_can_degrade_other_superuser_to_staff_user(
    admin_client, other_superuser
):
    form_data = get_default_edit_form_data(other_superuser)
    form_data.pop("is_superuser")

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": other_superuser.pk}),
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

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": other_superuser.pk}),
        data=form_data,
    )

    other_superuser.refresh_from_db()
    assert not other_superuser.is_staff
    assert not other_superuser.is_superuser


def test_superuser_can_promote_to_staff_user_to_superuser(admin_client, staffuser):
    form_data = get_default_edit_form_data(staffuser)
    form_data["is_superuser"] = "1"

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": staffuser.pk}),
        data=form_data,
    )

    staffuser.refresh_from_db()
    assert staffuser.is_staff
    assert staffuser.is_superuser


def test_superuser_can_promote_to_regular_user_to_staff_user(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_staff"] = "1"

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    user.refresh_from_db()
    assert user.is_staff
    assert not user.is_superuser


def test_superuser_can_promote_to_regular_user_to_superuser(admin_client, user):
    form_data = get_default_edit_form_data(user)
    form_data["is_staff"] = "1"
    form_data["is_superuser"] = "1"

    response = admin_client.post(
        reverse("misago:admin:users:accounts:edit", kwargs={"pk": user.pk}),
        data=form_data,
    )

    user.refresh_from_db()
    assert user.is_staff
    assert user.is_superuser


class UserAdminTests(AdminTestCase):
    def test_edit_view(self):
        """edit user view changes account"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "new_password": "newpass123",
                "staff_level": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertTrue(updated_user.check_password("newpass123"))
        self.assertEqual(updated_user.username, "NewUsername")
        self.assertEqual(updated_user.slug, "newusername")

        User.objects.get_by_username("NewUsername")
        User.objects.get_by_email("edited@example.com")

    def test_edit_dont_change_username(self):
        """
        If username wasn't changed, don't touch user's username, slug or history

        This is regression test for issue #640
        """
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            test_link,
            data={
                "username": "User",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(updated_user.username, "User")
        self.assertEqual(updated_user.slug, "user")
        self.assertEqual(updated_user.namechanges.count(), 0)

    def test_edit_change_password_whitespaces(self):
        """edit user view changes account password to include whitespaces"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "new_password": " newpass123 ",
                "staff_level": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertTrue(updated_user.check_password(" newpass123 "))
        self.assertEqual(updated_user.username, "NewUsername")
        self.assertEqual(updated_user.slug, "newusername")

        User.objects.get_by_username("NewUsername")
        User.objects.get_by_email("edited@example.com")

    def test_edit_disable_user(self):
        """edit user view allows admin to disable non admin"""
        self.user.is_superuser = False
        self.user.save()

        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, 'id="id_is_active_1"')
        self.assertContains(response, 'id="id_is_active_staff_message"')

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "is_staff": "0",
                "is_superuser": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
                "is_active": "0",
                "is_active_staff_message": "Disabled in test!",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertFalse(updated_user.is_active)
        self.assertEqual(updated_user.is_active_staff_message, "Disabled in test!")

    def test_edit_superuser_disable_admin(self):
        """edit user view allows admin to disable non admin"""
        self.user.is_superuser = True
        self.user.save()

        test_user = create_test_user("User", "user@example.com")

        test_user.is_staff = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, 'id="id_is_active_1"')
        self.assertContains(response, 'id="id_is_active_staff_message"')

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "is_staff": "1",
                "is_superuser": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
                "is_active": "0",
                "is_active_staff_message": "Disabled in test!",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertFalse(updated_user.is_active)
        self.assertEqual(updated_user.is_active_staff_message, "Disabled in test!")

    def test_edit_admin_cant_disable_admin(self):
        """edit user view disallows admin to disable admin"""
        self.user.is_superuser = False
        self.user.save()

        test_user = create_test_user("User", "user@example.com")

        test_user.is_staff = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertNotContains(response, 'id="id_is_active_1"')
        self.assertNotContains(response, 'id="id_is_active_staff_message"')

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "is_staff": "1",
                "is_superuser": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
                "is_active": "0",
                "is_active_staff_message": "Disabled in test!",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertTrue(updated_user.is_active)
        self.assertFalse(updated_user.is_active_staff_message)

    def test_edit_is_deleting_account_cant_reactivate(self):
        """users deleting own accounts can't be reactivated"""
        test_user = create_test_user("User", "user@example.com")
        test_user.mark_for_delete()

        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertNotContains(response, 'id="id_is_active_1"')
        self.assertNotContains(response, 'id="id_is_active_staff_message"')

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "is_staff": "1",
                "is_superuser": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
                "is_active": "1",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertFalse(updated_user.is_active)
        self.assertTrue(updated_user.is_deleting_account)

    def test_edit_unusable_password(self):
        """admin edit form handles unusable passwords and lets setting new password"""
        test_user = create_test_user("User", "user@example.com")
        self.assertFalse(test_user.has_usable_password())

        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, "alert-has-unusable-password")

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "new_password": "pass123",
                "is_staff": "1",
                "is_superuser": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
                "is_active": "1",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertTrue(updated_user.has_usable_password())

    def test_edit_keep_unusable_password(self):
        """
        admin edit form handles unusable passwords and lets admin leave them unchanged
        """
        test_user = create_test_user("User", "user@example.com")
        self.assertFalse(test_user.has_usable_password())

        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, "alert-has-unusable-password")

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "is_staff": "1",
                "is_superuser": "0",
                "signature": "Hello world!",
                "is_signature_locked": "1",
                "is_hiding_presence": "0",
                "limits_private_thread_invites_to": "0",
                "signature_lock_staff_message": "Staff message",
                "signature_lock_user_message": "User message",
                "subscribe_to_started_threads": "2",
                "subscribe_to_replied_threads": "2",
                "is_active": "1",
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertFalse(updated_user.has_usable_password())

    def test_edit_agreements_list(self):
        """edit view displays list of user's agreements"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            title="Test agreement!",
            text="Lorem ipsum!",
            is_active=True,
        )

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, agreement.title)

        save_user_agreement_acceptance(test_user, agreement, commit=True)

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, agreement.title)
