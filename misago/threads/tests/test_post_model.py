from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.forums.models import Forum

from misago.threads.checksums import update_post_checksum
from misago.threads.models import Thread, Post


class PostModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user("Bob", "bob@bob.com", "Pass.123")

        datetime = timezone.now()

        self.forum = Forum.objects.filter(role="forum")[:1][0]
        self.thread = Thread(
            forum=self.forum,
            started_on=datetime,
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=datetime,
            last_poster_name='Tester',
            last_poster_slug='tester')

        self.thread.set_title("Test thread")
        self.thread.save()

        self.post = Post.objects.create(
            forum=self.forum,
            thread=self.thread,
            poster=self.user,
            poster_name=self.user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime)

        update_post_checksum(self.post)
        self.post.save(update_fields=['checksum'])

        self.thread.first_post = self.post
        self.thread.last_post = self.post
        self.thread.save()

    def test_merge_invalid(self):
        """see if attempts for invalid merges fail"""
        with self.assertRaises(ValueError):
            self.post.merge(self.post)

        User = get_user_model()
        other_user = User.objects.create_user("Jeff", "Je@ff.com", "Pass.123")

        other_post = Post.objects.create(
            forum=self.forum,
            thread=self.thread,
            poster=other_user,
            poster_name=other_user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=timezone.now() + timedelta(minutes=5),
            updated_on=timezone.now() + timedelta(minutes=5))

        with self.assertRaises(ValueError):
            self.post.merge(other_post)

        other_thread = Thread.objects.create(
            forum=self.forum,
            started_on=timezone.now(),
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=timezone.now(),
            last_poster_name='Tester',
            last_poster_slug='tester')

        other_post = Post.objects.create(
            forum=self.forum,
            thread=other_thread,
            poster=self.user,
            poster_name=self.user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=timezone.now() + timedelta(minutes=5),
            updated_on=timezone.now() + timedelta(minutes=5))

        with self.assertRaises(ValueError):
            self.post.merge(other_post)

        other_post = Post.objects.create(
            forum=self.forum,
            thread=self.thread,
            poster_name=other_user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=timezone.now() + timedelta(minutes=5),
            updated_on=timezone.now() + timedelta(minutes=5))

        with self.assertRaises(ValueError):
            self.post.merge(other_post)
        with self.assertRaises(ValueError):
            other_post.merge(self.post)

    def test_merge(self):
        """merge method merges two posts into one"""
        other_post = Post.objects.create(
            forum=self.forum,
            thread=self.thread,
            poster=self.user,
            poster_name=self.user.username,
            poster_ip='127.0.0.1',
            original="I am other message!",
            parsed="<p>I am other message!</p>",
            checksum="nope",
            posted_on=timezone.now() + timedelta(minutes=5),
            updated_on=timezone.now() + timedelta(minutes=5))

        other_post.merge(self.post)

        self.assertIn(other_post.original, self.post.original)
        self.assertIn(other_post.parsed, self.post.parsed)
        self.assertTrue(self.post.is_valid)

    def test_move(self):
        """move method moves post to other thread"""
        new_thread = Thread.objects.create(
            forum=self.forum,
            started_on=timezone.now(),
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=timezone.now(),
            last_poster_name='Tester',
            last_poster_slug='tester')

        self.post.move(new_thread)

        self.assertEqual(self.post.thread, new_thread)
