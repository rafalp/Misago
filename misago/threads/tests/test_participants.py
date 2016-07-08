from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category

from ..models import Post, Thread, ThreadParticipant
from ..participants import (
    add_owner,
    make_thread_participants_aware,
    remove_participant,
    set_thread_owner,
    set_user_unread_private_threads_sync,
    thread_has_participants
)


class ParticipantsTests(TestCase):
    def setUp(self):
        datetime = timezone.now()

        self.category = Category.objects.all_categories()[:1][0]
        self.thread = Thread(
            category=self.category,
            started_on=datetime,
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=datetime,
            last_poster_name='Tester',
            last_poster_slug='tester'
        )

        self.thread.set_title("Test thread")
        self.thread.save()

        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster_name='Tester',
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime
        )

        self.thread.first_post = post
        self.thread.last_post = post
        self.thread.save()

    def test_thread_has_participants(self):
        """thread_has_participants returns true if thread has participants"""
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")
        other_user = User.objects.create_user(
            "Bob2", "bob2@boberson.com", "Pass.123")

        self.assertFalse(thread_has_participants(self.thread))

        ThreadParticipant.objects.add_participant(self.thread, user)
        self.assertTrue(thread_has_participants(self.thread))

        ThreadParticipant.objects.add_participant(self.thread, other_user)
        self.assertTrue(thread_has_participants(self.thread))

        self.thread.threadparticipant_set.all().delete()
        self.assertFalse(thread_has_participants(self.thread))

    def test_make_thread_participants_aware(self):
        """
        make_thread_participants_aware sets participants_list and participant
        adnotations on thread model
        """
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")
        other_user = User.objects.create_user(
            "Bob2", "bob2@boberson.com", "Pass.123")

        self.assertFalse(hasattr(self.thread, 'participants_list'))
        self.assertFalse(hasattr(self.thread, 'participant'))

        make_thread_participants_aware(user, self.thread)

        self.assertTrue(hasattr(self.thread, 'participants_list'))
        self.assertTrue(hasattr(self.thread, 'participant'))

        self.assertEqual(self.thread.participants_list, [])
        self.assertIsNone(self.thread.participant)

        ThreadParticipant.objects.add_participant(self.thread, user, True)
        ThreadParticipant.objects.add_participant(self.thread, other_user)

        make_thread_participants_aware(user, self.thread)

        self.assertEqual(self.thread.participant.user, user)
        for participant in self.thread.participants_list:
            if participant.user == user:
                break
        else:
            self.fail("thread.participants_list didn't contain user")

    def test_set_thread_owner(self):
        """set_thread_owner sets user as thread owner"""
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

        set_thread_owner(self.thread, user)

        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(user, owner.user)

    def test_set_user_unread_private_threads_sync(self):
        """
        set_user_unread_private_threads_sync sets sync_unread_private_threads
        flag on user model to true
        """
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

        self.assertFalse(user.sync_unread_private_threads)

        set_user_unread_private_threads_sync(user)
        self.assertTrue(user.sync_unread_private_threads)

        db_user = User.objects.get(pk=user.pk)
        self.assertTrue(db_user.sync_unread_private_threads)

    def test_add_owner(self):
        """add_owner adds user as thread owner"""
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

        add_owner(self.thread, user)
        self.assertTrue(user.sync_unread_private_threads)

        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(user, owner.user)

    def test_remove_participant(self):
        """remove_participant removes user from thread"""
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

        add_owner(self.thread, user)
        remove_participant(self.thread, user)

        with self.assertRaises(ThreadParticipant.DoesNotExist):
            self.thread.threadparticipant_set.get(user=user)

        set_user_unread_private_threads_sync(user)
        self.assertTrue(user.sync_unread_private_threads)

        db_user = User.objects.get(pk=user.pk)
        self.assertTrue(db_user.sync_unread_private_threads)
