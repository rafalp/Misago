from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category

from misago.threads.models import Thread, ThreadParticipant, Post


class ThreadParticipantTests(TestCase):
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

    def test_delete_participant(self):
        """delete_participant deletes participant from thread"""
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")
        other_user = User.objects.create_user(
            "Bob2", "bob2@boberson.com", "Pass.123")

        ThreadParticipant.objects.add_participant(self.thread, user)
        ThreadParticipant.objects.add_participant(self.thread, other_user)
        self.assertEqual(self.thread.participants.count(), 2)

        ThreadParticipant.objects.remove_participant(self.thread, user)
        self.assertEqual(self.thread.participants.count(), 1)

        with self.assertRaises(ThreadParticipant.DoesNotExist):
            participation = ThreadParticipant.objects.get(
                thread=self.thread, user=user)

    def test_add_participant(self):
        """add_participant adds participant to thread"""
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

        ThreadParticipant.objects.add_participant(self.thread, user)
        self.assertEqual(self.thread.participants.count(), 1)

        participation = ThreadParticipant.objects.get(
            thread=self.thread, user=user)
        self.assertFalse(participation.is_owner)

        ThreadParticipant.objects.add_participant(self.thread, user)
        self.assertEqual(self.thread.participants.count(), 2)

    def test_set_owner(self):
        """set_owner makes user thread owner"""
        User = get_user_model()
        user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

        ThreadParticipant.objects.set_owner(self.thread, user)
        self.assertEqual(self.thread.participants.count(), 1)

        participation = ThreadParticipant.objects.get(
            thread=self.thread, user=user)
        self.assertTrue(participation.is_owner)
        self.assertEqual(user, participation.user)

        other_user = User.objects.create_user(
            "Bob2", "bob2@boberson.com", "Pass.123")
        ThreadParticipant.objects.set_owner(self.thread, other_user)
        self.assertEqual(self.thread.participants.count(), 2)

        participation = ThreadParticipant.objects.get(
            thread=self.thread, user=user)
        self.assertFalse(participation.is_owner)

