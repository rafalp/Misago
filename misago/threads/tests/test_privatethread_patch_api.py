import json

from django.contrib.auth import get_user_model
from django.core import mail

from misago.acl.testutils import override_acl

from .. import testutils
from ..models import Thread, ThreadParticipant
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

    def test_add_empty_username(self):
        """path validates username"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(self.api_link, [
            {'op': 'add', 'path': 'participants', 'value': ''}
        ])

        self.assertContains(
            response, "You have to enter new participant's username.", status_code=400)

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

        self.other_user.email = 'rafio.xudb@gmail.com'
        self.other_user.save()

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
    def setUp(self):
        super(PrivateThreadRemoveParticipantApiTests, self).setUp()

        User = get_user_model()
        self.other_user = get_user_model().objects.create_user(
            'BobBoberson', 'bob@boberson.com', 'pass123')

    def test_remove_invalid(self):
        """removed user has to be participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(self.api_link, [
            {'op': 'remove', 'path': 'participants', 'value': 'string'}
        ])

        self.assertContains(
            response, "Participant to remove is invalid.", status_code=400)

    def test_remove_nonexistant(self):
        """removed user has to be participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(self.api_link, [
            {'op': 'remove', 'path': 'participants', 'value': self.other_user.pk}
        ])

        self.assertContains(
            response, "Participant doesn't exist.", status_code=400)

    def test_remove_not_owner(self):
        """api validates if user trying to remove other user is an owner"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(self.api_link, [
            {'op': 'remove', 'path': 'participants', 'value': self.other_user.pk}
        ])

        self.assertContains(
            response, "be thread owner to remove participants from it", status_code=400)

    def test_user_leave_thread(self):
        """api allows user to remove himself from thread"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(self.api_link, [
            {'op': 'remove', 'path': 'participants', 'value': self.user.pk}
        ])

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['deleted'])

        # thread still exists
        self.assertTrue(Thread.objects.get(pk=self.thread.pk))

        # leave event has valid type
        event = self.thread.post_set.order_by('id').last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, 'participant_left')

        # users were flagged for sync
        User = get_user_model()
        self.assertTrue(User.objects.get(pk=self.other_user.pk).sync_unread_private_threads)
        self.assertTrue(User.objects.get(pk=self.user.pk).sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 1)
        self.assertEqual(self.thread.participants.filter(pk=self.user.pk).count(), 0)

    def test_owner_remove_user(self):
        """api allows owner to remove other user"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        response = self.patch(self.api_link, [
            {'op': 'remove', 'path': 'participants', 'value': self.other_user.pk}
        ])

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['deleted'])

        # thread still exists
        self.assertTrue(Thread.objects.get(pk=self.thread.pk))

        # leave event has valid type
        event = self.thread.post_set.order_by('id').last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, 'participant_removed')

        # users were flagged for sync
        User = get_user_model()
        self.assertTrue(User.objects.get(pk=self.other_user.pk).sync_unread_private_threads)
        self.assertTrue(User.objects.get(pk=self.user.pk).sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 1)
        self.assertEqual(self.thread.participants.filter(pk=self.other_user.pk).count(), 0)

    def test_owner_leave_thread(self):
        """api allows owner to remove hisemf from thread, causing thread to close"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        response = self.patch(self.api_link, [
            {'op': 'remove', 'path': 'participants', 'value': self.user.pk}
        ])

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['deleted'])

        # thread still exists and is closed
        self.assertTrue(Thread.objects.get(pk=self.thread.pk).is_closed)

        # leave event has valid type
        event = self.thread.post_set.order_by('id').last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, 'owner_left')

        # users were flagged for sync
        User = get_user_model()
        self.assertTrue(User.objects.get(pk=self.other_user.pk).sync_unread_private_threads)
        self.assertTrue(User.objects.get(pk=self.user.pk).sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 1)
        self.assertEqual(self.thread.participants.filter(pk=self.user.pk).count(), 0)

    def test_last_user_leave_thread(self):
        """api allows last user leave thread, causing thread to delete"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(self.api_link, [
            {'op': 'remove', 'path': 'participants', 'value': self.user.pk}
        ])

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['deleted'])

        # thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # users were flagged for sync
        User = get_user_model()
        self.assertTrue(User.objects.get(pk=self.user.pk).sync_unread_private_threads)


class PrivateThreadTakeOverApiTests(PrivateThreadPatchApiTestCase):
    pass
