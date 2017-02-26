from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category
from misago.threads.checksums import update_post_checksum
from misago.threads.models import Post, Thread


UserModel = get_user_model()


class PostModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("Bob", "bob@bob.com", "Pass.123")

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

        self.post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=self.user,
            poster_name=self.user.username,
            poster_ip='127.0.0.1',
            original="Hello! I am test message!",
            parsed="<p>Hello! I am test message!</p>",
            checksum="nope",
            posted_on=datetime,
            updated_on=datetime,
        )

        update_post_checksum(self.post)
        self.post.save(update_fields=['checksum'])

        self.thread.first_post = self.post
        self.thread.last_post = self.post
        self.thread.save()

    def test_merge_invalid(self):
        """see if attempts for invalid merges fail"""
        # can't merge with itself
        with self.assertRaises(ValueError):
            self.post.merge(self.post)

        other_user = UserModel.objects.create_user("Jeff", "Je@ff.com", "Pass.123")

        other_thread = Thread.objects.create(
            category=self.category,
            started_on=timezone.now(),
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=timezone.now(),
            last_poster_name='Tester',
            last_poster_slug='tester',
        )

        # can't merge with other users posts
        with self.assertRaises(ValueError):
            self.post.merge(
                Post.objects.create(
                    category=self.category,
                    thread=self.thread,
                    poster=other_user,
                    poster_name=other_user.username,
                    poster_ip='127.0.0.1',
                    original="Hello! I am test message!",
                    parsed="<p>Hello! I am test message!</p>",
                    checksum="nope",
                    posted_on=timezone.now() + timedelta(minutes=5),
                    updated_on=timezone.now() + timedelta(minutes=5),
                )
            )

        # can't merge across threads
        with self.assertRaises(ValueError):
            self.post.merge(
                Post.objects.create(
                    category=self.category,
                    thread=other_thread,
                    poster=self.user,
                    poster_name=self.user.username,
                    poster_ip='127.0.0.1',
                    original="Hello! I am test message!",
                    parsed="<p>Hello! I am test message!</p>",
                    checksum="nope",
                    posted_on=timezone.now() + timedelta(minutes=5),
                    updated_on=timezone.now() + timedelta(minutes=5),
                )
            )

        # can't merge with events
        with self.assertRaises(ValueError):
            self.post.merge(
                Post.objects.create(
                    category=self.category,
                    thread=self.thread,
                    poster=self.user,
                    poster_name=self.user.username,
                    poster_ip='127.0.0.1',
                    original="Hello! I am test message!",
                    parsed="<p>Hello! I am test message!</p>",
                    checksum="nope",
                    posted_on=timezone.now() + timedelta(minutes=5),
                    updated_on=timezone.now() + timedelta(minutes=5),
                    is_event=True,
                )
            )

    def test_merge(self):
        """merge method merges two posts into one"""
        other_post = Post.objects.create(
            category=self.category,
            thread=self.thread,
            poster=self.user,
            poster_name=self.user.username,
            poster_ip='127.0.0.1',
            original="I am other message!",
            parsed="<p>I am other message!</p>",
            checksum="nope",
            posted_on=timezone.now() + timedelta(minutes=5),
            updated_on=timezone.now() + timedelta(minutes=5),
        )

        other_post.merge(self.post)

        self.assertIn(other_post.original, self.post.original)
        self.assertIn(other_post.parsed, self.post.parsed)
        self.assertTrue(self.post.is_valid)

    def test_move(self):
        """move method moves post to other thread"""
        new_thread = Thread.objects.create(
            category=self.category,
            started_on=timezone.now(),
            starter_name='Tester',
            starter_slug='tester',
            last_post_on=timezone.now(),
            last_poster_name='Tester',
            last_poster_slug='tester',
        )

        self.post.move(new_thread)

        self.assertEqual(self.post.thread, new_thread)
