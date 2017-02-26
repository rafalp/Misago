from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category
from misago.threads.models import Post, Thread, ThreadParticipant
from misago.threads.participants import (
    has_participants, make_participants_aware, set_owner, set_users_unread_private_threads_sync)


UserModel = get_user_model()


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
            last_poster_slug='tester',
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
            updated_on=datetime,
        )

        self.thread.first_post = post
        self.thread.last_post = post
        self.thread.save()

    def test_has_participants(self):
        """has_participants returns true if thread has participants"""
        users = [
            UserModel.objects.create_user("Bob", "bob@boberson.com", "Pass.123"),
            UserModel.objects.create_user("Bob2", "bob2@boberson.com", "Pass.123"),
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
        user = UserModel.objects.create_user("Bob", "bob@boberson.com", "Pass.123")
        other_user = UserModel.objects.create_user("Bob2", "bob2@boberson.com", "Pass.123")

        self.assertFalse(hasattr(self.thread, 'participants_list'))
        self.assertFalse(hasattr(self.thread, 'participant'))

        make_participants_aware(user, [self.thread])

        self.assertFalse(hasattr(self.thread, 'participants_list'))
        self.assertTrue(hasattr(self.thread, 'participant'))
        self.assertIsNone(self.thread.participant)

        ThreadParticipant.objects.set_owner(self.thread, user)
        ThreadParticipant.objects.add_participants(self.thread, [other_user])

        make_participants_aware(user, [self.thread])

        self.assertFalse(hasattr(self.thread, 'participants_list'))
        self.assertEqual(self.thread.participant.user, user)

    def test_make_thread_participants_aware(self):
        """
        make_participants_aware sets participants_list and participant
        annotations on thread model
        """
        user = UserModel.objects.create_user("Bob", "bob@boberson.com", "Pass.123")
        other_user = UserModel.objects.create_user("Bob2", "bob2@boberson.com", "Pass.123")

        self.assertFalse(hasattr(self.thread, 'participants_list'))
        self.assertFalse(hasattr(self.thread, 'participant'))

        make_participants_aware(user, self.thread)

        self.assertTrue(hasattr(self.thread, 'participants_list'))
        self.assertTrue(hasattr(self.thread, 'participant'))

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
        user = UserModel.objects.create_user("Bob", "bob@boberson.com", "Pass.123")

        set_owner(self.thread, user)

        owner = self.thread.threadparticipant_set.get(is_owner=True)
        self.assertEqual(user, owner.user)

    def test_set_users_unread_private_threads_sync(self):
        """
        set_users_unread_private_threads_sync sets sync_unread_private_threads
        flag on users provided to true
        """
        users = [
            UserModel.objects.create_user("Bob1", "bob1@boberson.com", "Pass.123"),
            UserModel.objects.create_user("Bob2", "bob2@boberson.com", "Pass.123"),
        ]

        set_users_unread_private_threads_sync(users=users)
        for user in users:
            UserModel.objects.get(
                pk=user.pk,
                sync_unread_private_threads=True,
            )

    def test_set_participants_unread_private_threads_sync(self):
        """
        set_users_unread_private_threads_sync sets sync_unread_private_threads
        flag on participants provided to true
        """
        users = [
            UserModel.objects.create_user("Bob1", "bob1@boberson.com", "Pass.123"),
            UserModel.objects.create_user("Bob2", "bob2@boberson.com", "Pass.123"),
        ]

        participants = [ThreadParticipant(user=u) for u in users]

        set_users_unread_private_threads_sync(participants=participants)
        for user in users:
            UserModel.objects.get(
                pk=user.pk,
                sync_unread_private_threads=True,
            )

    def test_set_participants_users_unread_private_threads_sync(self):
        """
        set_users_unread_private_threads_sync sets sync_unread_private_threads
        flag on users and participants provided to true
        """
        users = [
            UserModel.objects.create_user("Bob1", "bob1@boberson.com", "Pass.123"),
        ]

        participants = [ThreadParticipant(user=u) for u in users]

        users.append(UserModel.objects.create_user("Bob2", "bob2@boberson.com", "Pass.123"))

        set_users_unread_private_threads_sync(
            users=users,
            participants=participants,
        )
        for user in users:
            UserModel.objects.get(
                pk=user.pk,
                sync_unread_private_threads=True,
            )

    def test_set_users_unread_private_threads_sync_exclude_user(self):
        """exclude_user kwarg works"""
        users = [
            UserModel.objects.create_user("Bob1", "bob1@boberson.com", "Pass.123"),
            UserModel.objects.create_user("Bob2", "bob2@boberson.com", "Pass.123")
        ]

        set_users_unread_private_threads_sync(
            users=users,
            exclude_user=users[0],
        )

        self.assertFalse(UserModel.objects.get(pk=users[0].pk).sync_unread_private_threads)
        self.assertTrue(UserModel.objects.get(pk=users[1].pk).sync_unread_private_threads)

    def test_set_users_unread_private_threads_sync_noop(self):
        """excluding only user is noop"""
        user = UserModel.objects.create_user("Bob1", "bob1@boberson.com", "Pass.123")

        with self.assertNumQueries(0):
            set_users_unread_private_threads_sync(
                users=[user],
                exclude_user=user,
            )

        self.assertFalse(UserModel.objects.get(pk=user.pk).sync_unread_private_threads)
