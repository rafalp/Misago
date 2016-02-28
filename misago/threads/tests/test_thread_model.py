from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category

from misago.threads.models import Thread, ThreadParticipant, Post, Event


class ThreadModelTests(TestCase):
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

    def test_synchronize(self):
        """synchronize method updates thread data to reflect its contents"""
        User = get_user_model()
        user = User.objects.create_user("Bob", "bob@boberson.com", "Pass.123")

        self.assertEqual(self.thread.replies, 0)

        datetime = timezone.now() + timedelta(5)
        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime
        )

        # first sync call, updates last thread
        self.thread.synchronize()

        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertFalse(self.thread.has_moderated_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertFalse(self.thread.has_events)
        self.assertEqual(self.thread.replies, 1)

        # add moderated post
        moderated_post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime + timedelta(5),
            updated_on=datetime + timedelta(5),
            is_moderated=True
        )

        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertTrue(self.thread.has_moderated_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertFalse(self.thread.has_events)
        self.assertEqual(self.thread.replies, 1)

        # add hidden post
        hidden_post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime + timedelta(10),
            updated_on=datetime + timedelta(10),
            is_hidden=True
        )

        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, hidden_post)
        self.assertEqual(self.thread.last_post_on, hidden_post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertTrue(self.thread.has_moderated_posts)
        self.assertTrue(self.thread.has_hidden_posts)
        self.assertFalse(self.thread.has_events)
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
        self.assertTrue(self.thread.has_moderated_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertFalse(self.thread.has_events)
        self.assertEqual(self.thread.replies, 2)

        # unmoderate post
        moderated_post.is_moderated = False
        moderated_post.save()

        # last post not changed, but flags and count did
        self.thread.synchronize()
        self.assertEqual(self.thread.last_post, hidden_post)
        self.assertEqual(self.thread.last_post_on, hidden_post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)
        self.assertFalse(self.thread.has_reported_posts)
        self.assertFalse(self.thread.has_moderated_posts)
        self.assertFalse(self.thread.has_hidden_posts)
        self.assertFalse(self.thread.has_events)
        self.assertEqual(self.thread.replies, 3)

        # add event
        event = Event.objects.create(
            category=self.category,
            thread=self.thread,
            author_name=user.username,
            author_slug=user.slug,
            message="How bout nope?"
        )

        # sync set has_events flag
        self.thread.synchronize()
        self.assertTrue(self.thread.has_events)

        # sync unsetset has_events flag after only event was deleted
        event.delete()
        self.thread.synchronize()
        self.assertFalse(self.thread.has_events)

    def test_set_first_post(self):
        """set_first_post sets first post and poster data on thread"""
        User = get_user_model()
        user = User.objects.create_user("Bob", "bob@boberson.com", "Pass.123")

        datetime = timezone.now() + timedelta(5)

        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime
        )

        self.thread.set_first_post(post)
        self.assertEqual(self.thread.first_post, post)
        self.assertEqual(self.thread.started_on, post.posted_on)
        self.assertEqual(self.thread.starter, user)
        self.assertEqual(self.thread.starter_name, user.username)
        self.assertEqual(self.thread.starter_slug, user.slug)

    def test_set_last_post(self):
        """set_last_post sets first post and poster data on thread"""
        User = get_user_model()
        user = User.objects.create_user("Bob", "bob@boberson.com", "Pass.123")

        datetime = timezone.now() + timedelta(5)

        post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=user,
            poster_name=user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime
        )

        self.thread.set_last_post(post)
        self.assertEqual(self.thread.last_post, post)
        self.assertEqual(self.thread.last_post_on, post.posted_on)
        self.assertEqual(self.thread.last_poster, user)
        self.assertEqual(self.thread.last_poster_name, user.username)
        self.assertEqual(self.thread.last_poster_slug, user.slug)

    def test_move(self):
        """move(new_category) moves thread to other category"""
        # pick category instead of category (so we don't have to create one)
        root_category = Category.objects.root_category()
        Category(
            name='New Category',
            slug='new-category',
        ).insert_at(root_category, position='last-child', save=True)
        new_category = Category.objects.get(slug='new-category')

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
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=datetime,
            last_poster_name='Tester',
            last_poster_slug='tester'
        )

        other_thread.set_title("Other thread")
        other_thread.save()

        post = Post.objects.create(
            category=self.category,
            thread=other_thread,
            poster_name='Admin',
            poster_ip='127.0.0.1',
            original="Hello! I am other message!",
            parsed="<p>Hello! I am other message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime
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
        User = get_user_model()
        user_a = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")
        user_b = User.objects.create_user(
            "Weebl", "weebl@weeblson.com", "Pass.123")

        ThreadParticipant.objects.add_participant(self.thread, user_a)
        ThreadParticipant.objects.add_participant(self.thread, user_b)
        self.assertEqual(self.thread.participants.count(), 2)

        user_a.delete()
        Thread.objects.get(id=self.thread.id)

        user_b.delete()
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(id=self.thread.id)
