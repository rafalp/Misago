import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase

from .. import testutils
from ..models import Poll


class ThreadPollApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadPollApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(self.category, poster=self.user)
        self.override_acl()

        self.api_link = reverse('misago:api:thread-poll-list', kwargs={
            'thread_pk': self.thread.pk
        })

    def post(self, url, data=None):
        return self.client.post(url, json.dumps(data or {}), content_type='application/json')

    def put(self, url, data=None):
        return self.client.put(url, json.dumps(data or {}), content_type='application/json')

    def override_acl(self, user=None, category=None):
        new_acl = self.user.acl
        new_acl['categories'][self.category.pk].update({
            'can_see': 1,
            'can_browse': 1,
            'can_close_threads': 0,
        })

        new_acl.update({
            'can_start_polls': 1,
            'can_edit_polls': 1,
            'can_delete_polls': 1,
            'poll_edit_time': 0,
            'can_always_see_poll_voters': 0
        })

        if user:
            new_acl.update(user)
        if category:
            new_acl['categories'][self.category.pk].update(category)

        override_acl(self.user, new_acl)

    def mock_poll(self):
        self.poll = self.thread.poll = Poll.objects.create(
            category=self.category,
            thread=self.thread,
            poster=self.user,
            poster_name=self.user.username,
            poster_slug=self.user.slug,
            poster_ip='127.0.0.1',
            question="Lorem ipsum dolor met?",
            choices=[
                {
                    'hash': 'aaaaaaaaaaaa',
                    'label': 'Alpha',
                    'votes': 1
                },
                {
                    'hash': 'bbbbbbbbbbbb',
                    'label': 'Beta',
                    'votes': 0
                },
                {
                    'hash': 'gggggggggggg',
                    'label': 'Gamma',
                    'votes': 2
                },
                {
                    'hash': 'dddddddddddd',
                    'label': 'Delta',
                    'votes': 1
                }
            ],
            allowed_choices=2,
            votes=4
        )

        # one user voted for Alpha choice
        User = get_user_model()
        user = User.objects.create_user('bob', 'bob@test.com', 'Pass.123')

        self.poll.pollvote_set.create(
            category=self.category,
            thread=self.thread,
            voter=user,
            voter_name=user.username,
            voter_slug=user.slug,
            voter_ip='127.0.0.1',
            choice_hash='aaaaaaaaaaaa'
        )

        # test user voted on third and last choices
        self.poll.pollvote_set.create(
            category=self.category,
            thread=self.thread,
            voter=self.user,
            voter_name=self.user.username,
            voter_slug=self.user.slug,
            voter_ip='127.0.0.1',
            choice_hash='gggggggggggg'
        )
        self.poll.pollvote_set.create(
            category=self.category,
            thread=self.thread,
            voter=self.user,
            voter_name=self.user.username,
            voter_slug=self.user.slug,
            voter_ip='127.0.0.1',
            choice_hash='dddddddddddd'
        )

        # somebody else voted on third option before being deleted
        self.poll.pollvote_set.create(
            category=self.category,
            thread=self.thread,
            voter_name='deleted',
            voter_slug='deleted',
            voter_ip='127.0.0.1',
            choice_hash='gggggggggggg'
        )

        self.api_link = reverse('misago:api:thread-poll-detail', kwargs={
            'thread_pk': self.thread.pk,
            'pk': self.poll.pk
        })
