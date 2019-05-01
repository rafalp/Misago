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

User = get_user_model()


def test_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(reverse("misago:admin:index"))
    assert_contains(response, reverse("misago:admin:users:accounts:index"))


def test_list_renders_with_item(admin_client, users_admin_link, superuser):
    response = admin_client.get(users_admin_link)
    assert_contains(response, superuser.username)


class UserAdminTests(AdminTestCase):
    AJAX_HEADER = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}

    def test_new_view(self):
        """new user view creates account"""
        response = self.client.get(reverse("misago:admin:users:accounts:new"))
        self.assertEqual(response.status_code, 200)

        default_rank = Rank.objects.get_default()
        authenticated_role = Role.objects.get(special_role="authenticated")

        response = self.client.post(
            reverse("misago:admin:users:accounts:new"),
            data={
                "username": "NewUsername",
                "rank": str(default_rank.pk),
                "roles": str(authenticated_role.pk),
                "email": "edited@example.com",
                "new_password": "pass123",
                "staff_level": "0",
            },
        )
        self.assertEqual(response.status_code, 302)

        User.objects.get_by_username("NewUsername")
        test_user = User.objects.get_by_email("edited@example.com")

        self.assertTrue(test_user.check_password("pass123"))

    def test_new_view_password_with_whitespaces(self):
        """new user view creates account with whitespaces password"""
        response = self.client.get(reverse("misago:admin:users:accounts:new"))
        self.assertEqual(response.status_code, 200)

        default_rank = Rank.objects.get_default()
        authenticated_role = Role.objects.get(special_role="authenticated")

        response = self.client.post(
            reverse("misago:admin:users:accounts:new"),
            data={
                "username": "NewUsername",
                "rank": str(default_rank.pk),
                "roles": str(authenticated_role.pk),
                "email": "edited@example.com",
                "new_password": " pass123 ",
                "staff_level": "0",
            },
        )
        self.assertEqual(response.status_code, 302)

        User.objects.get_by_username("NewUsername")
        test_user = User.objects.get_by_email("edited@example.com")

        self.assertTrue(test_user.check_password(" pass123 "))

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

    def test_edit_make_admin(self):
        """edit user view allows super admin to make other user admin"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, 'id="id_is_staff_1"')
        self.assertContains(response, 'id="id_is_superuser_1"')

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
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertTrue(updated_user.is_staff)
        self.assertFalse(updated_user.is_superuser)

    def test_edit_make_superadmin_admin(self):
        """edit user view allows super admin to make other user super admin"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, 'id="id_is_staff_1"')
        self.assertContains(response, 'id="id_is_superuser_1"')

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "is_staff": "0",
                "is_superuser": "1",
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
        self.assertFalse(updated_user.is_staff)
        self.assertTrue(updated_user.is_superuser)

    def test_edit_denote_superadmin(self):
        """edit user view allows super admin to denote other super admin"""
        test_user = create_test_user(
            "User", "user@example.com", is_staff=True, is_superuser=True
        )

        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, 'id="id_is_staff_1"')
        self.assertContains(response, 'id="id_is_superuser_1"')

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
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.get(pk=test_user.pk)
        self.assertFalse(updated_user.is_staff)
        self.assertFalse(updated_user.is_superuser)

    def test_edit_cant_make_admin(self):
        """edit user view forbids admins from making other admins"""
        self.user.is_superuser = False
        self.user.save()

        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertNotContains(response, 'id="id_is_staff_1"')
        self.assertNotContains(response, 'id="id_is_superuser_1"')

        response = self.client.post(
            test_link,
            data={
                "username": "NewUsername",
                "rank": str(test_user.rank_id),
                "roles": str(test_user.roles.all()[0].pk),
                "email": "edited@example.com",
                "is_staff": "1",
                "is_superuser": "1",
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
        self.assertFalse(updated_user.is_staff)
        self.assertFalse(updated_user.is_superuser)

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
