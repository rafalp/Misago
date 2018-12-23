from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

from misago.acl.models import Role
from misago.admin.test import AdminTestCase
from misago.categories.models import Category
from misago.legal.models import Agreement
from misago.legal.utils import save_user_agreement_acceptance
from misago.threads.test import post_thread, reply_thread

from misago.users.datadownloads import request_user_data_download
from misago.users.models import Ban, DataDownload, Rank
from misago.users.test import create_test_user

User = get_user_model()


class UserAdminViewsTests(AdminTestCase):
    AJAX_HEADER = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}

    def test_link_registered(self):
        """admin index view contains users link"""
        response = self.client.get(reverse("misago:admin:index"))

        self.assertContains(response, reverse("misago:admin:users:accounts:index"))

    def test_list_view(self):
        """users list view returns 200"""
        response = self.client.get(reverse("misago:admin:users:accounts:index"))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response["location"])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_list_search(self):
        """users list is searchable"""
        response = self.client.get(reverse("misago:admin:users:accounts:index"))
        self.assertEqual(response.status_code, 302)

        link_base = response["location"]
        response = self.client.get(link_base)
        self.assertEqual(response.status_code, 200)

        user_a = create_test_user("Tyrael", "t123@test.com")
        user_b = create_test_user("Tyrion", "t321@test.com")
        user_c = create_test_user("Karen", "t432@test.com")

        # Search both
        response = self.client.get("%s&username=tyr" % link_base)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_a.username)
        self.assertContains(response, user_b.username)

        # Search tyrion
        response = self.client.get("%s&username=tyrion" % link_base)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user_a.username)
        self.assertContains(response, user_b.username)

        # Search tyrael
        response = self.client.get("%s&email=t123@test.com" % link_base)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_a.username)
        self.assertNotContains(response, user_b.username)

        # Search disabled
        user_c.is_active = False
        user_c.save()

        response = self.client.get("%s&disabled=1" % link_base)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user_a.username)
        self.assertNotContains(response, user_b.username)
        self.assertContains(response, "<del>%s</del>" % user_c.username)

        # Search requested own account delete
        user_c.is_deleting_account = True
        user_c.save()

        response = self.client.get("%s&is_deleting_account=1" % link_base)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user_a.username)
        self.assertNotContains(response, user_b.username)
        self.assertContains(response, "<del>%s</del>" % user_c.username)

        response = self.client.get("%s&disabled=1" % link_base)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user_a.username)
        self.assertNotContains(response, user_b.username)
        self.assertContains(response, "<del>%s</del>" % user_c.username)

    def test_mass_activation(self):
        """users list activates multiple users"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user(
                "User%s" % i, "user%s@example.com" % i, requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "activate", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        inactive_qs = User.objects.filter(id__in=user_pks, requires_activation=1)
        self.assertEqual(inactive_qs.count(), 0)
        self.assertIn("has been activated", mail.outbox[0].subject)

    def test_mass_ban(self):
        """users list bans multiple users"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user(
                "User%s" % i, "user%s@example.com" % i, requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "ban", "selected_items": user_pks},
        )
        self.assertNotContains(response, 'value="ip"')
        self.assertNotContains(response, 'value="ip_first"')
        self.assertNotContains(response, 'value="ip_two"')

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={
                "action": "ban",
                "selected_items": user_pks,
                "ban_type": ["usernames", "emails", "domains"],
                "finalize": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ban.objects.count(), 21)

    def test_mass_ban_with_ips(self):
        """users list bans multiple users that also have ips"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user(
                "User%s" % i,
                "user%s@example.com" % i,
                joined_from_ip="73.95.67.27",
                requires_activation=1,
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "ban", "selected_items": user_pks},
        )
        self.assertContains(response, 'value="ip"')
        self.assertContains(response, 'value="ip_first"')
        self.assertContains(response, 'value="ip_two"')

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={
                "action": "ban",
                "selected_items": user_pks,
                "ban_type": [
                    "usernames",
                    "emails",
                    "domains",
                    "ip",
                    "ip_first",
                    "ip_two",
                ],
                "finalize": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ban.objects.count(), 24)

    def test_mass_request_data_download(self):
        """users list requests data download for multiple users"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user(
                "User%s" % i, "user%s@example.com" % i, requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "request_data_download", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DataDownload.objects.filter(user_id__in=user_pks).count(), len(user_pks)
        )

    def test_mass_request_data_download_avoid_excessive_downloads(self):
        """users list avoids excessive data download requests for multiple users"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user(
                "User%s" % i, "user%s@example.com" % i, requires_activation=1
            )
            request_user_data_download(test_user)
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "v", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DataDownload.objects.filter(user_id__in=user_pks).count(), len(user_pks)
        )

    def test_mass_delete_accounts_self(self):
        """its impossible to delete oneself"""
        user_pks = [self.user.pk]

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_accounts", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response["location"])
        self.assertContains(response, "delete yourself")

    def test_mass_delete_accounts_admin(self):
        """its impossible to delete admin account"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user("User%s" % i, "user%s@example.com" % i)
            user_pks.append(test_user.pk)

            test_user.is_staff = True
            test_user.save()

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_accounts", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response["location"])
        self.assertContains(response, "is admin and can")
        self.assertContains(response, "be deleted.")

        self.assertEqual(User.objects.count(), 11)

    def test_mass_delete_accounts_superadmin(self):
        """its impossible to delete superadmin account"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user("User%s" % i, "user%s@example.com" % i)
            user_pks.append(test_user.pk)

            test_user.is_superuser = True
            test_user.save()

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_accounts", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response["location"])
        self.assertContains(response, "is admin and can")
        self.assertContains(response, "be deleted.")

        self.assertEqual(User.objects.count(), 11)

    def test_mass_delete_accounts(self):
        """users list deletes users"""
        # create 10 users to delete
        user_pks = []
        for i in range(10):
            test_user = create_test_user(
                "User%s" % i, "user%s@example.com" % i, requires_activation=0
            )
            user_pks.append(test_user.pk)

        # create 10 more users that won't be deleted
        for i in range(10):
            test_user = create_test_user(
                "Weebl%s" % i, "weebl%s@test.com" % i, requires_activation=0
            )

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_accounts", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 11)

    def test_mass_delete_all_self(self):
        """its impossible to delete oneself with content"""
        user_pks = [self.user.pk]

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_all", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response["location"])
        self.assertContains(response, "delete yourself")

    def test_mass_delete_all_admin(self):
        """its impossible to delete admin account and content"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user("User%s" % i, "user%s@example.com" % i)
            user_pks.append(test_user.pk)

            test_user.is_staff = True
            test_user.save()

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_all", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response["location"])
        self.assertContains(response, "is admin and can")
        self.assertContains(response, "be deleted.")

        self.assertEqual(User.objects.count(), 11)

    def test_mass_delete_all_superadmin(self):
        """its impossible to delete superadmin account and content"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user("User%s" % i, "user%s@example.com" % i)
            user_pks.append(test_user.pk)

            test_user.is_superuser = True
            test_user.save()

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_all", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response["location"])
        self.assertContains(response, "is admin and can")
        self.assertContains(response, "be deleted.")

        self.assertEqual(User.objects.count(), 11)

    def test_mass_delete_all(self):
        """users list mass deleting view has no showstoppers"""
        user_pks = []
        for i in range(10):
            test_user = create_test_user(
                "User%s" % i, "user%s@example.com" % i, requires_activation=1
            )
            user_pks.append(test_user.pk)

        response = self.client.post(
            reverse("misago:admin:users:accounts:index"),
            data={"action": "delete_all", "selected_items": user_pks},
        )
        self.assertEqual(response.status_code, 200)
        # asser that no user has been deleted, because actuall deleting happens in
        # dedicated views called via ajax from JavaScript
        self.assertEqual(User.objects.count(), 11)

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
        self.assertContains(response, 'id="div_id_has_usable_password"')

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
        """admin edit form handles unusable passwords and lets admin leave them unchanged"""
        test_user = create_test_user("User", "user@example.com")
        self.assertFalse(test_user.has_usable_password())

        test_link = reverse(
            "misago:admin:users:accounts:edit", kwargs={"pk": test_user.pk}
        )

        response = self.client.get(test_link)
        self.assertContains(response, 'id="div_id_has_usable_password"')

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

    def test_delete_threads_view_self(self):
        """delete user threads view validates if user deletes self"""
        test_link = reverse(
            "misago:admin:users:accounts:delete-threads", kwargs={"pk": self.user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "delete yourself")

    def test_delete_threads_view_staff(self):
        """delete user threads view validates if user deletes staff"""
        test_user = create_test_user("User", "user@example.com")
        test_user.is_staff = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:delete-threads", kwargs={"pk": test_user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "is admin and")

    def test_delete_threads_view_superuser(self):
        """delete user threads view validates if user deletes superuser"""
        test_user = create_test_user("User", "user@example.com")
        test_user.is_superuser = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:delete-threads", kwargs={"pk": test_user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "is admin and")

    def test_delete_threads_view(self):
        """delete user threads view deletes threads"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:delete-threads", kwargs={"pk": test_user.pk}
        )

        category = Category.objects.all_categories()[:1][0]
        [post_thread(category, poster=test_user) for _ in range(10)]

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        self.assertEqual(response_dict["deleted_count"], 10)
        self.assertFalse(response_dict["is_completed"])

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        self.assertEqual(response_dict["deleted_count"], 0)
        self.assertTrue(response_dict["is_completed"])

    def test_delete_posts_view_self(self):
        """delete user posts view validates if user deletes self"""
        test_link = reverse(
            "misago:admin:users:accounts:delete-posts", kwargs={"pk": self.user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "delete yourself")

    def test_delete_posts_view_staff(self):
        """delete user posts view validates if user deletes staff"""
        test_user = create_test_user("User", "user@example.com")
        test_user.is_staff = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:delete-posts", kwargs={"pk": test_user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "is admin and")

    def test_delete_posts_view_superuser(self):
        """delete user posts view validates if user deletes superuser"""
        test_user = create_test_user("User", "user@example.com")
        test_user.is_superuser = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:delete-posts", kwargs={"pk": test_user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "is admin and")

    def test_delete_posts_view(self):
        """delete user posts view deletes posts"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:delete-posts", kwargs={"pk": test_user.pk}
        )

        category = Category.objects.all_categories()[:1][0]
        thread = post_thread(category)
        [reply_thread(thread, poster=test_user) for _ in range(10)]

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        self.assertEqual(response_dict["deleted_count"], 10)
        self.assertFalse(response_dict["is_completed"])

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        self.assertEqual(response_dict["deleted_count"], 0)
        self.assertTrue(response_dict["is_completed"])

    def test_delete_account_view_self(self):
        """delete user account view validates if user deletes self"""
        test_link = reverse(
            "misago:admin:users:accounts:delete-account", kwargs={"pk": self.user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "delete yourself")

    def test_delete_account_view_staff(self):
        """delete user account view validates if user deletes staff"""
        test_user = create_test_user("User", "user@example.com")
        test_user.is_staff = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:delete-account", kwargs={"pk": test_user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "is admin and")

    def test_delete_account_view_superuser(self):
        """delete user account view validates if user deletes superuser"""
        test_user = create_test_user("User", "user@example.com")
        test_user.is_superuser = True
        test_user.save()

        test_link = reverse(
            "misago:admin:users:accounts:delete-account", kwargs={"pk": test_user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse("misago:admin:index"))
        self.assertContains(response, "is admin and")

    def test_delete_account_view(self):
        """delete user account view deletes user account"""
        test_user = create_test_user("User", "user@example.com")
        test_link = reverse(
            "misago:admin:users:accounts:delete-account", kwargs={"pk": test_user.pk}
        )

        response = self.client.post(test_link, **self.AJAX_HEADER)
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        self.assertTrue(response_dict["is_completed"])
