from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import testutils
from misago.threads.models import ThreadParticipant


class ThreadParticipantsTests(AuthenticatedUserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def setUp(self):
        super(ThreadParticipantsTests, self).setUp()

        self.forum = Forum.objects.private_threads()
        self.thread = testutils.post_thread(self.forum)

    def test_participants_list(self):
        """participants list displays thread participants"""
        User = get_user_model()
        users = (
            User.objects.create_user("Bob", "bob@bob.com", "pass123"),
            User.objects.create_user("Dam", "dam@bob.com", "pass123")
        )

        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participant(self.thread, users[0])
        ThreadParticipant.objects.add_participant(self.thread, users[1])

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_participants', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug
        })

        response = self.client.get(link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        owner_pos = response.content.find(self.user.get_absolute_url())
        for user in users:
            participant_pos = response.content.find(user.get_absolute_url())
            self.assertTrue(owner_pos < participant_pos)
