import json

from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadPollApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadPollApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(self.category, poster=self.user)
        self.override_acl()

        self.api_link = reverse(
            'misago:api:thread-poll-list', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

    def post(self, url, data=None):
        return self.client.post(url, json.dumps(data or {}), content_type='application/json')

    def put(self, url, data=None):
        return self.client.put(url, json.dumps(data or {}), content_type='application/json')

    def override_acl(self, user=None, category=None):
        new_acl = self.user.acl_cache
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
            'can_always_see_poll_voters': 0,
        })

        if user:
            new_acl.update(user)
        if category:
            new_acl['categories'][self.category.pk].update(category)

        override_acl(self.user, new_acl)

    def mock_poll(self):
        self.poll = self.thread.poll = testutils.post_poll(self.thread, self.user)

        self.api_link = reverse(
            'misago:api:thread-poll-detail',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.poll.pk,
            }
        )
