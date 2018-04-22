from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.threads import testutils
from misago.threads.models import Thread, ThreadParticipant

from .test_privatethreads import PrivateThreadsTestCase


class PrivateThreadsListApiTests(PrivateThreadsTestCase):
    def setUp(self):
        super(PrivateThreadsListApiTests, self).setUp()

        self.api_link = reverse('misago:api:private-thread-list')

    def test_unauthenticated(self):
        """api requires user to sign in and be able to access it"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You have to sign in to use private threads.",
        })

    def test_no_permission(self):
        """api requires user to have permission to be able to access it"""
        override_acl(self.user, {'can_use_private_threads': 0})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't use private threads.",
        })

    def test_empty_list(self):
        """api has no showstoppers on returning empty list"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'], [])

    def test_thread_visibility(self):
        """only participated threads are returned by private threads api"""
        visible = testutils.post_thread(category=self.category, poster=self.user)
        reported = testutils.post_thread(category=self.category, poster=self.user)

        # hidden thread
        testutils.post_thread(category=self.category, poster=self.user)

        ThreadParticipant.objects.add_participants(visible, [self.user])

        reported.has_reported_posts = True
        reported.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['count'], 1)
        self.assertEqual(response_json['results'][0]['id'], visible.id)

        # threads with reported posts will also show to moderators
        override_acl(self.user, {'can_moderate_private_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['count'], 2)
        self.assertEqual(response_json['results'][0]['id'], reported.id)
        self.assertEqual(response_json['results'][1]['id'], visible.id)


class PrivateThreadRetrieveApiTests(PrivateThreadsTestCase):
    def setUp(self):
        super(PrivateThreadRetrieveApiTests, self).setUp()

        self.thread = testutils.post_thread(self.category, poster=self.user)
        self.api_link = self.thread.get_api_url()

    def test_anonymous(self):
        """anonymous user can't see private thread"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You have to sign in to use private threads.",
        })

    def test_no_permission(self):
        """user needs to have permission to see private thread"""
        override_acl(self.user, {'can_use_private_threads': 0})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't use private threads.",
        })

    def test_no_participant(self):
        """user cant see thread he isn't part of"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_mod_not_reported(self):
        """moderator can't see private thread that has no reports"""
        override_acl(self.user, {'can_moderate_private_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_reported_not_mod(self):
        """non-mod can't see private thread that has reported posts"""
        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_can_see_owner(self):
        """user can see thread he is owner of"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['title'], self.thread.title)
        self.assertEqual(
            response_json['participants'], [
                {
                    'id': self.user.id,
                    'username': self.user.username,
                    'slug': self.user.slug,
                    'avatars': self.user.avatars,
                    'is_owner': True,
                },
            ]
        )

    def test_can_see_participant(self):
        """user can see thread he is participant of"""
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['title'], self.thread.title)
        self.assertEqual(
            response_json['participants'], [
                {
                    'id': self.user.id,
                    'username': self.user.username,
                    'slug': self.user.slug,
                    'avatars': self.user.avatars,
                    'is_owner': False,
                },
            ]
        )

    def test_mod_can_see_reported(self):
        """moderator can see private thread that has reports"""
        override_acl(self.user, {'can_moderate_private_threads': 1})

        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['title'], self.thread.title)
        self.assertEqual(response_json['participants'], [])


class PrivateThreadDeleteApiTests(PrivateThreadsTestCase):
    def setUp(self):
        super(PrivateThreadDeleteApiTests, self).setUp()

        self.thread = testutils.post_thread(self.category, poster=self.user)
        self.api_link = self.thread.get_api_url()

        ThreadParticipant.objects.add_participants(self.thread, [self.user])

    def test_delete_thread_no_permission(self):
        """api tests permission to delete threads"""
        self.override_acl({'can_hide_threads': 0})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't delete threads in this category.",
        })

        self.override_acl({'can_hide_threads': 1})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't delete threads in this category.",
        })

    def test_delete_thread(self):
        """DELETE to API link with permission deletes thread"""
        self.override_acl({'can_hide_threads': 2})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)
