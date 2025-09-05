from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .. import test
from ...categories.models import Category
from ...polls.models import Poll
from ...posts.models import Post
from ...privatethreadmembers.models import PrivateThreadMember
from ...users.test import create_test_user
from ..models import Thread


def test_thread_model_set_first_post():
    pass


class ThreadModelTests(TestCase):
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

        Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster_name="Tester",
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            posted_at=datetime,
            updated_at=datetime,
        )

        self.thread.synchronize()
        self.thread.save()

    def test_set_first_post(self):
        """set_first_post sets first post and poster data on thread"""
        user = create_test_user("User", "user@example.com")

        datetime = timezone.now() + timedelta(5)

        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            posted_at=datetime,
            updated_at=datetime,
        )

        self.thread.set_first_post(post)
        self.assertEqual(self.thread.first_post, post)
        self.assertEqual(self.thread.started_on, post.posted_at)
        self.assertEqual(self.thread.starter, user)
        self.assertEqual(self.thread.starter_name, user.username)
        self.assertEqual(self.thread.starter_slug, user.slug)

    def test_set_last_post(self):
        """set_last_post sets first post and poster data on thread"""
        user = create_test_user("User", "user@example.com")

        datetime = timezone.now() + timedelta(5)

        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            posted_at=datetime,
            updated_at=datetime,
        )

        self.thread.set_last_post(post)
        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_at)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)

    def test_set_best_answer(self):
        """set_best_answer sets best answer and setter data on thread"""
        user = create_test_user("User", "user@example.com")

        best_answer = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            posted_at=timezone.now(),
            updated_at=timezone.now(),
            is_protected=True,
        )

        self.thread.synchronize()
        self.thread.save()

        self.thread.set_best_answer(user, best_answer)
        self.thread.save()

        self.assertEqual(self.thread.best_answer, best_answer)
        self.assertTrue(self.thread.has_best_answer)
        self.assertTrue(self.thread.best_answer_is_protected)
        self.assertTrue(self.thread.best_answer_marked_on)
        self.assertEqual(self.thread.best_answer_marked_by, user)
        self.assertEqual(self.thread.best_answer_marked_by_name, user.username)
        self.assertEqual(self.thread.best_answer_marked_by_slug, user.slug)

        # clear best answer
        self.thread.clear_best_answer()

        self.assertIsNone(self.thread.best_answer)
        self.assertFalse(self.thread.has_best_answer)
        self.assertFalse(self.thread.best_answer_is_protected)
        self.assertIsNone(self.thread.best_answer_marked_on)
        self.assertIsNone(self.thread.best_answer_marked_by)
        self.assertIsNone(self.thread.best_answer_marked_by_name)
        self.assertIsNone(self.thread.best_answer_marked_by_slug)

    def test_set_invalid_best_answer(self):
        """set_best_answer implements some assertions for data integrity"""
        user = create_test_user("User", "user@example.com")

        other_thread = test.post_thread(self.category)
        with self.assertRaises(ValueError):
            self.thread.set_best_answer(user, other_thread.first_post)

        with self.assertRaises(ValueError):
            self.thread.set_best_answer(user, self.thread.first_post)

        with self.assertRaises(ValueError):
            reply = test.reply_thread(self.thread, is_hidden=True)
            self.thread.set_best_answer(user, reply)

        with self.assertRaises(ValueError):
            reply = test.reply_thread(self.thread, is_unapproved=True)
            self.thread.set_best_answer(user, reply)


def test_thread_private_thread_member_ids_property_returns_list_of_private_thread_member_ids(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    private_thread_member_ids = list(thread.private_thread_member_ids)
    assert private_thread_member_ids == [other_user.id, user.id]


def test_thread_private_thread_owner_id_property_returns_id_of_private_thread_owner(
    thread, user, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=user)
    PrivateThreadMember.objects.create(thread=thread, user=other_user, is_owner=True)

    assert thread.private_thread_owner_id == other_user.id


def test_thread_private_thread_owner_id_property_returns_none_if_thread_has_no_members(
    thread,
):
    assert thread.private_thread_owner_id is None


def test_thread_private_thread_owner_id_property_returns_none_if_thread_has_no_owner(
    thread, other_user
):
    PrivateThreadMember.objects.create(thread=thread, user=other_user)
    assert thread.private_thread_owner_id is None
