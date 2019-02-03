from django.urls import reverse

from .. import test
from ...acl.test import patch_user_acl
from ..models import Thread, ThreadParticipant
from ..test import patch_private_threads_acl
from .test_privatethreads import PrivateThreadsTestCase


class PrivateThreadsListApiTests(PrivateThreadsTestCase):
    def setUp(self):
        super().setUp()

        self.api_link = reverse("misago:api:private-thread-list")

    def test_unauthenticated(self):
        """api requires user to sign in and be able to access it"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have to sign in to use private threads."}
        )

    @patch_user_acl({"can_use_private_threads": False})
    def test_no_permission(self):
        """api requires user to have permission to be able to access it"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't use private threads."})

    @patch_user_acl({"can_use_private_threads": True})
    def test_empty_list(self):
        """api has no showstoppers on returning empty list"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json["results"]), 0)

    @patch_user_acl({"can_use_private_threads": True})
    def test_thread_visibility(self):
        """only participated threads are returned by private threads api"""
        visible = test.post_thread(category=self.category, poster=self.user)
        reported = test.post_thread(category=self.category, poster=self.user)

        # hidden thread
        test.post_thread(category=self.category, poster=self.user)

        ThreadParticipant.objects.add_participants(visible, [self.user])

        reported.has_reported_posts = True
        reported.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json["results"]), 1)
        self.assertEqual(response_json["results"][0]["id"], visible.id)

        # threads with reported posts will also show to moderators
        with patch_user_acl({"can_moderate_private_threads": True}):
            response = self.client.get(self.api_link)
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertEqual(len(response_json["results"]), 2)
            self.assertEqual(response_json["results"][0]["id"], reported.id)
            self.assertEqual(response_json["results"][1]["id"], visible.id)


class PrivateThreadRetrieveApiTests(PrivateThreadsTestCase):
    def setUp(self):
        super().setUp()

        self.thread = test.post_thread(self.category, poster=self.user)
        self.api_link = self.thread.get_api_url()

    def test_anonymous(self):
        """anonymous user can't see private thread"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have to sign in to use private threads."}
        )

    @patch_user_acl({"can_use_private_threads": False})
    def test_no_permission(self):
        """user needs to have permission to see private thread"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't use private threads."})

    @patch_user_acl({"can_use_private_threads": True})
    def test_no_participant(self):
        """user cant see thread he isn't part of"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    @patch_user_acl(
        {"can_use_private_threads": True, "can_moderate_private_threads": True}
    )
    def test_mod_not_reported(self):
        """moderator can't see private thread that has no reports"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    @patch_user_acl(
        {"can_use_private_threads": True, "can_moderate_private_threads": False}
    )
    def test_reported_not_mod(self):
        """non-mod can't see private thread that has reported posts"""
        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    @patch_user_acl({"can_use_private_threads": True})
    def test_can_see_owner(self):
        """user can see thread he is owner of"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["title"], self.thread.title)
        self.assertEqual(
            response_json["participants"],
            [
                {
                    "id": self.user.id,
                    "username": self.user.username,
                    "avatars": self.user.avatars,
                    "url": self.user.get_absolute_url(),
                    "is_owner": True,
                }
            ],
        )

    @patch_user_acl({"can_use_private_threads": True})
    def test_can_see_participant(self):
        """user can see thread he is participant of"""
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["title"], self.thread.title)
        self.assertEqual(
            response_json["participants"],
            [
                {
                    "id": self.user.id,
                    "username": self.user.username,
                    "avatars": self.user.avatars,
                    "url": self.user.get_absolute_url(),
                    "is_owner": False,
                }
            ],
        )

    @patch_user_acl(
        {"can_use_private_threads": True, "can_moderate_private_threads": True}
    )
    def test_mod_can_see_reported(self):
        """moderator can see private thread that has reports"""
        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["title"], self.thread.title)
        self.assertEqual(response_json["participants"], [])


class PrivateThreadDeleteApiTests(PrivateThreadsTestCase):
    def setUp(self):
        super().setUp()

        self.thread = test.post_thread(self.category, poster=self.user)
        self.api_link = self.thread.get_api_url()

        ThreadParticipant.objects.add_participants(self.thread, [self.user])

    @patch_private_threads_acl({"can_hide_threads": 0})
    def test_hide_thread_no_permission(self):
        """api tests permission to delete threads"""

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"], "You can't delete threads in this category."
        )

    @patch_private_threads_acl({"can_hide_threads": 1})
    def test_delete_thread_no_permission(self):
        """api tests permission to delete threads"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"], "You can't delete threads in this category."
        )

    @patch_private_threads_acl({"can_hide_threads": 2})
    def test_delete_thread(self):
        """DELETE to API link with permission deletes thread"""
        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)
