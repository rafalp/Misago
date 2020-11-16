from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .. import test
from ...categories.models import Category
from ...users.test import create_test_user
from ..models import Poll, Post, Thread, ThreadParticipant


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
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        self.thread.synchronize()
        self.thread.save()

    def test_synchronize(self):
        """synchronize method updates thread data to reflect its contents"""
        user = create_test_user("User", "user@example.com")

        self.assertEqual(self.thread.replies, 0)

        datetime = timezone.now() + timedelta(5)
        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        # first sync call, updates last thread
        self.thread.synchronize()

        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertFalse(self.thread.has_unapproved_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertEqual(self.thread.replies, 1)

        # add unapproved post
        unapproved_post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime + timedelta(5),
            updated_on=datetime + timedelta(5),
            is_unapproved=True,
        )

        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertTrue(self.thread.has_unapproved_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertEqual(self.thread.replies, 1)

        # add hidden post
        hidden_post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime + timedelta(10),
            updated_on=datetime + timedelta(10),
            is_hidden=True,
        )

        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, hidden_post)
        self.assertEqual(self.thread.last_post_on, hidden_post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertTrue(self.thread.has_unapproved_posts)
        self.assertTrue(self.thread.has_hidden_posts)
        self.assertEqual(self.thread.replies, 2)

        # unhide post
        hidden_post.is_hidden = False
        hidden_post.save()

        # last post changed to unhidden one
        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, hidden_post)
        self.assertEqual(self.thread.last_post_on, hidden_post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertTrue(self.thread.has_unapproved_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertEqual(self.thread.replies, 2)

        # unmoderate post
        unapproved_post.is_unapproved = False
        unapproved_post.save()

        # last post not changed, but flags and count did
        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, hidden_post)
        self.assertEqual(self.thread.last_post_on, hidden_post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertFalse(self.thread.has_unapproved_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertEqual(self.thread.replies, 3)

        # add event post
        event = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="-",
            parsed="-",
            checksum="nope",
            posted_on=datetime + timedelta(10),
            updated_on=datetime + timedelta(10),
            is_event=True,
        )

        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, event)
        self.assertEqual(self.thread.last_post_on, event.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertTrue(self.thread.last_post_is_event)
        self.assertTrue(self.thread.has_events)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertFalse(self.thread.has_unapproved_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        # events don't count to reply count
        self.assertEqual(self.thread.replies, 3)

        # create another post to provoke other has_events resolution path
        Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        self.thread.synchronize()
        self.assertFalse(self.thread.last_post_is_event)
        self.assertTrue(self.thread.has_events)

        # remove event
        event.delete()

        self.thread.synchronize()
        self.assertFalse(self.thread.last_post_is_event)
        self.assertFalse(self.thread.has_events)

        # has poll flag
        self.assertFalse(self.thread.has_poll)

        Poll.objects.create(
            thread=self.thread,
            category=self.category,
            poster_name="test",
            poster_slug="test",
            choices=[],
        )

        self.thread.synchronize()
        self.assertTrue(self.thread.has_poll)

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
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        self.thread.set_first_post(post)
        self.assertEqual(self.thread.first_post, post)
        self.assertEqual(self.thread.started_on, post.posted_on)
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
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        self.thread.set_last_post(post)
        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_on)
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
            checksum="nope",
            posted_on=timezone.now(),
            updated_on=timezone.now(),
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

    def test_move(self):
        """move(new_category) moves thread to other category"""
        root_category = Category.objects.root_category()
        Category(name="New Category", slug="new-category").insert_at(
            root_category, position="last-child", save=True
        )
        new_category = Category.objects.get(slug="new-category")

        self.thread.move(new_category)
        self.assertEqual(self.thread.category, new_category)

        for post in self.thread.post_set.all():
            self.assertEqual(post.category_id, new_category.id)

    def test_merge(self):
        """merge(other_thread) moves other thread content to this thread"""
        with self.assertRaises(ValueError):
            self.thread.merge(self.thread)

        datetime = timezone.now() + timedelta(5)

        other_thread = Thread(
            category=self.category,
            started_on=datetime,
            starter_name="Tester",
            starter_slug="tester",
            last_post_on=datetime,
            last_poster_name="Tester",
            last_poster_slug="tester",
        )

        other_thread.set_title("Other thread")
        other_thread.save()

        post = Post.objects.create(
            category=self.category,
            thread=other_thread,
            poster_name="Admin",
            original="Hello! I am other message!",
            parsed="<p>Hello! I am other message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        other_thread.first_post = post
        other_thread.last_post = post
        other_thread.save()

        self.thread.merge(other_thread)

        self.thread.synchronize()
        self.assertEqual(self.thread.replies, 1)
        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_on)
        self.assertEqual(self.thread.last_poster_name, "Admin")
        self.assertEqual(self.thread.last_poster_slug, "admin")

    def test_delete_private_thread(self):
        """
        private thread gets deleted automatically
        when there are no participants left in it
        """
        user = create_test_user("User", "user@example.com")
        other_user = create_test_user("OtherUser", "otheruser@example.com")

        ThreadParticipant.objects.add_participants(self.thread, [user, other_user])
        self.assertEqual(self.thread.participants.count(), 2)

        user.delete(anonymous_username="Deleted")
        Thread.objects.get(id=self.thread.id)

        other_user.delete(anonymous_username="Deleted")
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(id=self.thread.id)
