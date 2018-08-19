from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from misago.threads.models import Poll, PollVote, Thread

from .test_thread_poll_api import ThreadPollApiTestCase


class ThreadPollDeleteTests(ThreadPollApiTestCase):
    def setUp(self):
        super(ThreadPollDeleteTests, self).setUp()

        self.mock_poll()

    def test_anonymous(self):
        """api requires you to sign in to delete poll"""
        self.logout_user()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_invalid_thread_id(self):
        """api validates that thread id is integer"""
        api_link = reverse(
            'misago:api:thread-poll-detail',
            kwargs={
                'thread_pk': 'kjha6dsa687sa',
                'pk': self.poll.pk,
            }
        )

        response = self.client.delete(api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_thread_id(self):
        """api validates that thread exists"""
        api_link = reverse(
            'misago:api:thread-poll-detail',
            kwargs={
                'thread_pk': self.thread.pk + 1,
                'pk': self.poll.pk,
            }
        )

        response = self.client.delete(api_link)
        self.assertEqual(response.status_code, 404)

    def test_invalid_poll_id(self):
        """api validates that poll id is integer"""
        api_link = reverse(
            'misago:api:thread-poll-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': 'sad98as7d97sa98',
            }
        )

        response = self.client.delete(api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_poll_id(self):
        """api validates that poll exists"""
        api_link = reverse(
            'misago:api:thread-poll-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.poll.pk + 123,
            }
        )

        response = self.client.delete(api_link)
        self.assertEqual(response.status_code, 404)

    def test_no_permission(self):
        """api validates that user has permission to delete poll in thread"""
        self.override_acl({'can_delete_polls': 0})

        response = self.client.delete(self.api_link)
        self.assertContains(response, "can't delete polls", status_code=403)

    def test_no_permission_timeout(self):
        """api validates that user's window to delete poll in thread has closed"""
        self.override_acl({'can_delete_polls': 1, 'poll_edit_time': 5})

        self.poll.posted_on = timezone.now() - timedelta(minutes=15)
        self.poll.save()

        response = self.client.delete(self.api_link)
        self.assertContains(
            response, "can't delete polls that are older than 5 minutes", status_code=403
        )

    def test_no_permission_poll_closed(self):
        """api validates that user's window to delete poll in thread has closed"""
        self.override_acl({'can_delete_polls': 1})

        self.poll.posted_on = timezone.now() - timedelta(days=15)
        self.poll.length = 5
        self.poll.save()

        response = self.client.delete(self.api_link)
        self.assertContains(response, "This poll is over", status_code=403)

    def test_no_permission_other_user_poll(self):
        """api validates that user has permission to delete other user poll in thread"""
        self.override_acl({'can_delete_polls': 1})

        self.poll.poster = None
        self.poll.save()

        response = self.client.delete(self.api_link)
        self.assertContains(response, "can't delete other users polls", status_code=403)

    def test_no_permission_closed_thread(self):
        """api validates that user has permission to delete poll in closed thread"""
        self.override_acl(category={'can_close_threads': 0})

        self.thread.is_closed = True
        self.thread.save()

        response = self.client.delete(self.api_link)
        self.assertContains(response, "thread is closed", status_code=403)

        self.override_acl(category={'can_close_threads': 1})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_no_permission_closed_category(self):
        """api validates that user has permission to delete poll in closed category"""
        self.override_acl(category={'can_close_threads': 0})

        self.category.is_closed = True
        self.category.save()

        response = self.client.delete(self.api_link)
        self.assertContains(response, "category is closed", status_code=403)

        self.override_acl(category={'can_close_threads': 1})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_poll_delete(self):
        """api deletes poll and associated votes"""
        response = self.client.delete(self.api_link)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'can_start_poll': True})

        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(PollVote.objects.count(), 0)

        # api set poll flag on thread to False
        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.has_poll)

    def test_other_user_poll_delete(self):
        """api deletes other user's poll and associated votes, even if its over"""
        self.override_acl({'can_delete_polls': 2, 'poll_edit_time': 5})

        self.poll.poster = None
        self.poll.posted_on = timezone.now() - timedelta(days=15)
        self.poll.length = 5
        self.poll.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'can_start_poll': True})

        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(PollVote.objects.count(), 0)

        # api set poll flag on thread to False
        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertFalse(thread.has_poll)
