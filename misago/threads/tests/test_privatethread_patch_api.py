import json

from django.contrib.auth import get_user_model
from django.core import mail

from misago.acl.testutils import override_acl

from .. import testutils
from ..models import ThreadParticipant
from .test_privatethreads import PrivateThreadsTestCase


class PrivateThreadPatchApiTestCase(PrivateThreadsTestCase):
    def setUp(self):
        super(PrivateThreadPatchApiTestCase, self).setUp()

        self.thread = testutils.post_thread(self.category, poster=self.user)
        self.api_link = self.thread.get_api_url()

    def patch(self, api_link, ops):
        return self.client.patch(
            api_link, json.dumps(ops), content_type="application/json")


class PrivateThreadAddParticipantApiTests(PrivateThreadPatchApiTestCase):
    def setUp(self):
        super(PrivateThreadAddParticipantApiTests, self).setUp()

        User = get_user_model()
        self.other_user = get_user_model().objects.create_user(
            'BobBoberson', 'bob@boberson.com', 'pass123')

    def test_add_participant_not_owner(self):
        """non-owner can't add participant"""
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(self.api_link, [
            {'op': 'add', 'path': 'participants', 'value': self.user.username}
        ])
        self.assertContains(
            response, "be thread owner to add new participants to it", status_code=400)

    def test_add_nonexistant_user(self):
        """can't user two times"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(self.api_link, [
            {'op': 'add', 'path': 'participants', 'value': 'InvalidUser'}
        ])

        self.assertContains(response, "No user with such name exists.", status_code=400)

    def test_add_already_participant(self):
        """can't add user that is already participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(self.api_link, [
            {'op': 'add', 'path': 'participants', 'value': self.user.username}
        ])

        self.assertContains(
            response, "This user is already thread participant", status_code=400)

    def test_add_blocking_user(self):
        """can't add user that is already participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        self.other_user.blocks.add(self.user)

        response = self.patch(self.api_link, [
            {'op': 'add', 'path': 'participants', 'value': self.other_user.username}
        ])
        self.assertContains(response, "BobBoberson is blocking you.", status_code=400)

    def test_add_too_many_users(self):
        """can't add user that is already participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        User = get_user_model()
        for i in range(self.user.acl['max_private_thread_participants']):
            user = User.objects.create_user(
                'User{}'.format(i), 'user{}@example.com'.format(i), 'Pass.123')
            ThreadParticipant.objects.add_participants(self.thread, [user])

        response = self.patch(self.api_link, [
            {'op': 'add', 'path': 'participants', 'value': self.other_user.username}
        ])
        self.assertContains(
            response, "You can't add any more new users to this thread.", status_code=400)

    def test_add_user(self):
        """adding user to thread add user to thread as participant, sets event and emails him"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(self.api_link, [
            {'op': 'add', 'path': 'participants', 'value': self.other_user.username}
        ])
        self.assertEqual(response.json()['participant'], {
            'id': self.other_user.id,
            'username': self.other_user.username,
            'avatar_hash': self.other_user.avatar_hash,
            'url': self.other_user.get_absolute_url(),
            'is_owner': False,
        })

        # event was set on thread
        event = self.thread.post_set.order_by('id').last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, 'added_participant')

        # notification about new private thread was sent to other user
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[-1]

        self.assertIn(self.user.username, email.subject)
        self.assertIn(self.thread.title, email.subject)


class PrivateThreadRemoveParticipantApiTests(PrivateThreadPatchApiTestCase):
    pass


class PrivateThreadTakeOverApiTests(PrivateThreadPatchApiTestCase):
    pass
