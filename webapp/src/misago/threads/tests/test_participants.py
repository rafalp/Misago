from django.test import TestCase
from django.utils import timezone

from ...categories.models import Category
from ...users.test import create_test_user
from ..models import Post, Thread, ThreadParticipant
from ..participants import (
    has_participants,
    make_participants_aware,
    set_owner,
    set_users_unread_private_threads_sync,
)


class ParticipantsTests(TestCase):
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

    def test_has_participants(self):
        """has_participants returns true if thread has participants"""
        users = [
            create_test_user("User", "user@example.com"),
            create_test_user("OtherUser", "otheruser@example.com"),
        ]

        self.assertFalse(has_participants(self.thread))

        ThreadParticipant.objects.add_participants(self.thread, users)
        self.assertTrue(has_participants(self.thread))

        self.thread.threadparticipant_set.all().delete()
        self.assertFalse(has_participants(self.thread))

    def test_make_threads_participants_aware(self):
        """
        make_participants_aware sets participants_list and participant
        annotations on list of threads
        """
        user = create_test_user("User", "user@example.com")
        other_user = create_test_user("OtherUser", "otheruser@example.com")

        self.assertFalse(hasattr(self.thread, "participants_list"))
        self.assertFalse(hasattr(self.thread, "participant"))

        make_participants_aware(user, [self.thread])

        self.assertFalse(hasattr(self.thread, "participants_list"))
        self.assertTrue(hasattr(self.thread, "participant"))
        self.assertIsNone(self.thread.participant)

        ThreadParticipant.objects.set_owner(self.thread, user)
        ThreadParticipant.objects.add_participants(self.thread, [other_user])

        make_participants_aware(user, [self.thread])

        self.assertFalse(hasattr(self.thread, "participants_list"))
        self.assertEqual(self.thread.participant.user, user)

    def test_make_thread_participants_aware(self):
        """
        make_participants_aware sets participants_list and participant
        annotations on thread model
        """
        user = create_test_user("User", "user@example.com")
        other_user = create_test_user("OtherUser", "otheruser@example.com")

        self.assertFalse(hasattr(self.thread, "participants_list"))
        self.assertFalse(hasattr(self.thread, "participant"))

        make_participants_aware(user, self.thread)

        self.assertTrue(hasattr(self.thread, "participants_list"))
        self.assertTrue(hasattr(self.thread, "participant"))

        self.assertEqual(self.thread.participants_list, [])
        self.assertIsNone(self.thread.participant)

        ThreadParticipant.objects.set_owner(self.thread, user)
        ThreadParticipant.objects.add_participants(self.thread, [other_user])

        make_participants_aware(user, self.thread)

        self.assertEqual(self.thread.participant.user, user)
        for participant in self.thread.participants_list:
            if participant.user == user:
                break
        else:
            self.fail("thread.participants_list didn't contain user")

    def test_set_owner(self):
        """set_owner sets user as thread owner"""
        user = create_test_user("User", "user@example.com")

        set_owner(self.thread, user)

        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(user, owner.user)

    def test_set_users_unread_private_threads_sync(self):
        """
        set_users_unread_private_threads_sync sets sync_unread_private_threads
        flag on users provided to true
        """
        users = [
            create_test_user("User", "user@example.com"),
            create_test_user("OtherUser", "otheruser@example.com"),
        ]

        set_users_unread_private_threads_sync(users=users)
        for user in users:
            user.refresh_from_db()
            assert user.sync_unread_private_threads

    def test_set_participants_unread_private_threads_sync(self):
        """
        set_users_unread_private_threads_sync sets sync_unread_private_threads
        flag on participants provided to true
        """
        users = [
            create_test_user("User", "user@example.com"),
            create_test_user("OtherUser", "otheruser@example.com"),
        ]

        participants = [ThreadParticipant(user=u) for u in users]

        set_users_unread_private_threads_sync(participants=participants)
        for user in users:
            user.refresh_from_db()
            assert user.sync_unread_private_threads

    def test_set_participants_users_unread_private_threads_sync(self):
        """
        set_users_unread_private_threads_sync sets sync_unread_private_threads
        flag on users and participants provided to true
        """
        users = [create_test_user("User", "user@example.com")]
        participants = [ThreadParticipant(user=u) for u in users]
        users.append(create_test_user("OtherUser", "otheruser@example.com"))

        set_users_unread_private_threads_sync(users=users, participants=participants)
        for user in users:
            user.refresh_from_db()
            assert user.sync_unread_private_threads

    def test_set_users_unread_private_threads_sync_exclude_user(self):
        """exclude_user kwarg works"""
        users = [
            create_test_user("User", "user@example.com"),
            create_test_user("OtherUser", "otheruser@example.com"),
        ]

        set_users_unread_private_threads_sync(users=users, exclude_user=users[0])

        [i.refresh_from_db() for i in users]
        assert users[0].sync_unread_private_threads is False
        assert users[1].sync_unread_private_threads

    def test_set_users_unread_private_threads_sync_noop(self):
        """excluding only user is noop"""
        user = create_test_user("User", "user@example.com")

        with self.assertNumQueries(0):
            set_users_unread_private_threads_sync(users=[user], exclude_user=user)

        user.refresh_from_db()
        assert user.sync_unread_private_threads is False
