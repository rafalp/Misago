from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from ..models import Poll, PollVote
from .test_thread_poll_api import ThreadPollApiTestCase


class ThreadGetVotesTests(ThreadPollApiTestCase):
    def setUp(self):
        super(ThreadGetVotesTests, self).setUp()

        self.mock_poll()

        self.api_link = reverse('misago:api:thread-poll-votes', kwargs={
            'thread_pk': self.thread.pk,
            'pk': self.poll.pk
        })

    def test_anonymous(self):
        """api allows guests to get poll votes"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_no_permission(self):
        """api chcecks permission to see poll voters"""
        self.override_acl({
            'can_always_see_poll_voters': False
        })

        self.poll.is_public = False
        self.poll.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_nonpublic_poll(self):
        """api validates that poll is public"""
        self.logout_user()

        self.poll.is_public = False
        self.poll.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_get_votes(self):
        """api returns list of votes"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 4)

        self.assertEqual([c['label'] for c in response_json], ['Alpha', 'Beta', 'Gamma', 'Delta'])
        self.assertEqual([c['votes'] for c in response_json], [1, 0, 2, 1])
        self.assertEqual([len(c['voters']) for c in response_json], [1, 0, 2, 1])

        self.assertEqual([[v['username'] for v in c['voters']] for c in response_json], [
            ['bob'],
            [],
            [self.user.username, 'deleted'],
            [self.user.username]
        ])

        User = get_user_model()
        user =  User.objects.get(slug='bob')

        self.assertEqual([[v['url'] for v in c['voters']] for c in response_json], [
            [user.get_absolute_url()],
            [],
            [self.user.get_absolute_url(), None],
            [self.user.get_absolute_url()]
        ])


class ThreadPostVotesTests(ThreadPollApiTestCase):
    def setUp(self):
        super(ThreadPostVotesTests, self).setUp()

        self.mock_poll()

        self.api_link = reverse('misago:api:thread-poll-votes', kwargs={
            'thread_pk': self.thread.pk,
            'pk': self.poll.pk
        })

    def test_anonymous(self):
        """api requires you to sign in to vote in poll"""
        self.logout_user()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
