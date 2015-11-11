from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import testutils
from misago.threads.models import Thread, ThreadParticipant


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

    def test_edit_participants(self):
        """edit participants view displays thread participants"""
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

        link = reverse('misago:private_thread_edit_participants', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug
        })

        response = self.client.get(link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        owner_pos = response.content.find(self.user.get_absolute_url())
        for user in users:
            participant_pos = response.content.find(user.get_absolute_url())
            self.assertTrue(owner_pos < participant_pos)

    def test_owner_remove_participant(self):
        """remove participant allows owner to remove participant"""
        User = get_user_model()
        other_user = User.objects.create_user("Bob", "bob@bob.com", "pass123")

        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participant(self.thread, other_user)

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_remove_participant', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug,
            'user_id': other_user.id,
        })

        response = self.client.post(link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.thread.threadparticipant_set.count(), 1)
        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(owner.user, self.user)

        Thread.objects.get(pk=self.thread.pk)
        self.thread.threadparticipant_set.get(user=self.user)

    def test_owner_remove_non_participant(self):
        """remove participant handles attempt to remove invalid participant"""
        User = get_user_model()
        other_user = User.objects.create_user("Bob", "bob@bob.com", "pass123")

        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participant(self.thread, other_user)

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_remove_participant', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug,
            'user_id': 123456,
        })

        response = self.client.post(link, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.thread.threadparticipant_set.count(), 2)
        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(owner.user, self.user)

        Thread.objects.get(pk=self.thread.pk)
        self.thread.threadparticipant_set.get(user=self.user)

    def test_non_owner_remove_participant(self):
        """non-owner cant remove participant"""
        User = get_user_model()
        other_user = User.objects.create_user("Bob", "bob@bob.com", "pass123")

        ThreadParticipant.objects.set_owner(self.thread, other_user)
        ThreadParticipant.objects.add_participant(self.thread, self.user)

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_remove_participant', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug,
            'user_id': other_user.pk,
        })

        response = self.client.post(link, **self.ajax_header)
        self.assertEqual(response.status_code, 406)

        self.assertEqual(self.thread.threadparticipant_set.count(), 2)
        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(owner.user, other_user)

        Thread.objects.get(pk=self.thread.pk)
        self.thread.threadparticipant_set.get(user=self.user)

    def test_owner_add_participant(self):
        """owner can add participants"""
        User = get_user_model()
        users = (
            User.objects.create_user("Bob", "bob@bob.com", "pass123"),
            User.objects.create_user("Dam", "dam@bob.com", "pass123")
        )

        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participant(self.thread, users[0])

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_add_participants', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug,
        })

        response = self.client.post(link, data={
            'users': 'Bob, Dam'
        }, **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.thread.threadparticipant_set.count(), 3)
        for participant in self.thread.threadparticipant_set.all():
            if participant.is_owner:
                self.assertEqual(participant.user, self.user)
            else:
                self.assertIn(participant.user, users)

        Thread.objects.get(pk=self.thread.pk)
        self.thread.threadparticipant_set.get(user=self.user)

    def test_non_owner_add_participant(self):
        """non-owner cant add participants"""
        User = get_user_model()
        users = (
            User.objects.create_user("Bob", "bob@bob.com", "pass123"),
            User.objects.create_user("Dam", "dam@bob.com", "pass123")
        )

        ThreadParticipant.objects.set_owner(self.thread, users[0])
        ThreadParticipant.objects.add_participant(self.thread, self.user)

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_add_participants', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug,
        })

        response = self.client.post(link, data={
            'users': 'Bob, Dam'
        }, **self.ajax_header)
        self.assertEqual(response.status_code, 406)

    def test_owner_leave_thread_new_owner(self):
        """
        leave thread view makes owner leave thread and makes new user owner
        """
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

        link = reverse('misago:private_thread_leave', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug
        })

        response = self.client.post(link, **self.ajax_header)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.thread.threadparticipant_set.count(), 2)
        new_owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertNotEqual(new_owner.user, self.user)
        self.assertIn(new_owner.user, users)

        Thread.objects.get(pk=self.thread.pk)
        with self.assertRaises(ThreadParticipant.DoesNotExist):
            self.thread.threadparticipant_set.get(user=self.user)

    def test_owner_leave_thread_delete(self):
        """
        leave thread view makes owner leave thread and deletes abadoned thread
        """
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_leave', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug
        })

        response = self.client.post(link, **self.ajax_header)
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        with self.assertRaises(ThreadParticipant.DoesNotExist):
            self.thread.threadparticipant_set.get(user=self.user)

    def test_participant_leave_thread(self):
        """
        leave thread view makes user leave thread
        """
        User = get_user_model()
        users = (
            User.objects.create_user("Bob", "bob@bob.com", "pass123"),
            User.objects.create_user("Dam", "dam@bob.com", "pass123")
        )

        ThreadParticipant.objects.set_owner(self.thread, users[0])
        ThreadParticipant.objects.add_participant(self.thread, users[1])
        ThreadParticipant.objects.add_participant(self.thread, self.user)

        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        link = reverse('misago:private_thread_leave', kwargs={
            'thread_id': self.thread.id,
            'thread_slug': self.thread.slug
        })

        response = self.client.post(link, **self.ajax_header)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.thread.threadparticipant_set.count(), 2)
        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(owner.user, users[0])

        for participants in self.thread.threadparticipant_set.all():
            self.assertIn(participants.user, users)

        Thread.objects.get(pk=self.thread.pk)
        with self.assertRaises(ThreadParticipant.DoesNotExist):
            self.thread.threadparticipant_set.get(user=self.user)
