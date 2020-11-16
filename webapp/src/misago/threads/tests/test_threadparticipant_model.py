from django.test import TestCase
from django.utils import timezone

from ...categories.models import Category
from ...users.test import create_test_user
from ..models import Post, Thread, ThreadParticipant


class ThreadParticipantTests(TestCase):
    def setUp(self):
        datetime = timezone.now()

        self.category = Category.objects.all_categories()[:1][0]
        self.thread = Thread(
            category=self.category,
            started_on=datetime,
            starter_name="Tester",
            starter_slug="tester",
            last_post_on=datetime,
            last_poster_name="Tester",
            last_poster_slug="tester",
        )

        self.thread.set_title("Test thread")
        self.thread.save()

        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster_name="Tester",
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        self.thread.first_post = post
        self.thread.last_post = post
        self.thread.save()

    def test_set_owner(self):
        """set_owner makes user thread owner"""
        user = create_test_user("User", "user@example.com")
        other_user = create_test_user("User2", "user2@example.com")

        ThreadParticipant.objects.set_owner(self.thread, user)
        self.assertEqual(self.thread.participants.count(), 1)

        participant = ThreadParticipant.objects.get(thread=self.thread, user=user)
        self.assertTrue(participant.is_owner)
        self.assertEqual(user, participant.user)

        # threads can't have more than one owner
        ThreadParticipant.objects.set_owner(self.thread, other_user)
        self.assertEqual(self.thread.participants.count(), 2)

        participant = ThreadParticipant.objects.get(thread=self.thread, user=user)
        self.assertFalse(participant.is_owner)

        self.assertEqual(ThreadParticipant.objects.filter(is_owner=True).count(), 1)

    def test_add_participants(self):
        """add_participant adds participant to thread"""
        users = [
            create_test_user("User", "user@example.com"),
            create_test_user("User2", "user2@example.com"),
        ]

        ThreadParticipant.objects.add_participants(self.thread, users)
        self.assertEqual(self.thread.participants.count(), 2)

        for user in users:
            participant = ThreadParticipant.objects.get(thread=self.thread, user=user)
            self.assertFalse(participant.is_owner)

    def test_remove_participant(self):
        """remove_participant deletes participant from thread"""
        user = create_test_user("User", "user@example.com")
        other_user = create_test_user("User2", "user2@example.com")

        ThreadParticipant.objects.add_participants(self.thread, [user])
        ThreadParticipant.objects.add_participants(self.thread, [other_user])
        self.assertEqual(self.thread.participants.count(), 2)

        ThreadParticipant.objects.remove_participant(self.thread, user)
        self.assertEqual(self.thread.participants.count(), 1)

        with self.assertRaises(ThreadParticipant.DoesNotExist):
            ThreadParticipant.objects.get(thread=self.thread, user=user)
