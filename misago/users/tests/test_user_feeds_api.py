from django.urls import reverse

from misago.threads import testutils
from misago.threads.tests.test_threads_api import ThreadsApiTestCase


class UserThreadsApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(UserThreadsApiTests, self).setUp()

        self.api_link = reverse(
            'misago:api:user-threads', kwargs={
                'pk': self.user.pk,
            }
        )

    def test_invalid_user_id(self):
        """api validates user id"""
        link = reverse(
            'misago:api:user-threads', kwargs={
                'pk': 'abcd',
            }
        )
        response = self.client.get(link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_user_id(self):
        """api validates that user for id exists"""
        link = reverse(
            'misago:api:user-threads', kwargs={
                'pk': self.user.pk + 1,
            }
        )
        response = self.client.get(link)
        self.assertEqual(response.status_code, 404)

    def test_empty_response(self):
        """api has no showstopers on empty response"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user_post(self):
        """user post doesn't show in feed because its not first post in thread"""
        testutils.reply_thread(self.thread, poster=self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user_event(self):
        """events don't show in feeds at all"""
        testutils.reply_thread(
            self.thread,
            poster=self.user,
            is_event=True,
        )

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user_thread(self):
        """user thread shows in feed"""
        thread = testutils.post_thread(
            category=self.category,
            poster=self.user,
        )

        # this post will not show in feed
        testutils.reply_thread(thread, poster=self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['id'], thread.first_post_id)

    def test_user_thread_anonymous(self):
        """user thread shows in feed requested by unauthenticated user"""
        thread = testutils.post_thread(
            category=self.category,
            poster=self.user,
        )

        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['id'], thread.first_post_id)


class UserPostsApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(UserPostsApiTests, self).setUp()

        self.api_link = reverse(
            'misago:api:user-posts', kwargs={
                'pk': self.user.pk,
            }
        )

    def test_invalid_user_id(self):
        """api validates user id"""
        link = reverse(
            'misago:api:user-posts', kwargs={
                'pk': 'abcd',
            }
        )
        response = self.client.get(link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_user_id(self):
        """api validates that user for id exists"""
        link = reverse(
            'misago:api:user-posts', kwargs={
                'pk': self.user.pk + 1,
            }
        )
        response = self.client.get(link)
        self.assertEqual(response.status_code, 404)

    def test_empty_response(self):
        """api has no showstopers on empty response"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user_event(self):
        """events don't show in feeds at all"""
        testutils.reply_thread(
            self.thread,
            poster=self.user,
            is_event=True,
        )

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user_hidden_post(self):
        """hidden posts don't show in feeds at all"""
        testutils.reply_thread(
            self.thread,
            poster=self.user,
            is_hidden=True,
        )

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user_unapproved_post(self):
        """unapproved posts don't show in feeds at all"""
        testutils.reply_thread(
            self.thread,
            poster=self.user,
            is_unapproved=True,
        )

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

    def test_user_posts(self):
        """user posts show in feed"""
        post = testutils.reply_thread(self.thread, poster=self.user)
        other_post = testutils.reply_thread(self.thread, poster=self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results'][0]['id'], other_post.pk)
        self.assertEqual(response.json()['results'][1]['id'], post.pk)

    def test_user_thread(self):
        """user thread shows in feed"""
        thread = testutils.post_thread(
            category=self.category,
            poster=self.user,
        )
        post = testutils.reply_thread(thread, poster=self.user)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results'][0]['id'], post.pk)
        self.assertEqual(response.json()['results'][1]['id'], thread.first_post_id)

    def test_user_post_anonymous(self):
        """user post shows in feed requested by unauthenticated user"""
        post = testutils.reply_thread(self.thread, poster=self.user)
        other_post = testutils.reply_thread(self.thread, poster=self.user)

        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results'][0]['id'], other_post.pk)
        self.assertEqual(response.json()['results'][1]['id'], post.pk)

    def test_user_thread_anonymous(self):
        """user thread shows in feed requested by unauthenticated user"""
        thread = testutils.post_thread(
            category=self.category,
            poster=self.user,
        )
        post = testutils.reply_thread(thread, poster=self.user)

        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json()['results'][0]['id'], post.pk)
        self.assertEqual(response.json()['results'][1]['id'], thread.first_post_id)
