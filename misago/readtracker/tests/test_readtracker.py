from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from misago.acl import add_acl
from misago.categories.models import Category
from misago.readtracker import categoriestracker, threadstracker
from misago.threads import testutils
from misago.users.models import AnonymousUser


UserModel = get_user_model()


class ReadTrackerTests(TestCase):
    def setUp(self):
        self.categories = list(Category.objects.all_categories()[:1])
        self.category = self.categories[0]

        self.user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")
        self.anon = AnonymousUser()

    def post_thread(self, datetime):
        return testutils.post_thread(
            category=self.category,
            started_on=datetime,
        )


class CategoriesTrackerTests(ReadTrackerTests):
    def test_anon_empty_category_read(self):
        """anon users content is always read"""
        categoriestracker.make_read_aware(self.anon, self.categories)
        self.assertIsNone(self.category.last_post_on)
        self.assertTrue(self.category.is_read)

    def test_anon_category_recent_reply_read(self):
        """anon users content is always read"""
        categoriestracker.make_read_aware(self.anon, self.categories)
        self.category.last_post_on = timezone.now()
        self.assertTrue(self.category.is_read)

    def test_empty_category_is_read(self):
        """empty category is read for signed in user"""
        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

    def test_make_read_aware_sets_read_flag_for_empty_category(self):
        """make_read_aware sets read flag on empty category"""
        categoriestracker.make_read_aware(self.anon, self.categories)
        self.assertTrue(self.category.is_read)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

    def test_make_read_aware_sets_read_flag_for_category_old_thread(self):
        """make_read_aware sets read flag on category with old thread"""
        self.category.last_post_on = self.user.joined_on - timedelta(days=1)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

    def test_make_read_aware_sets_unread_flag_for_category_new_thread(self):
        """make_read_aware sets unread flag on category with new thread"""
        self.category.last_post_on = self.user.joined_on + timedelta(days=1)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

    def test_sync_record_for_empty_category(self):
        """sync_record sets read flag on empty category"""
        add_acl(self.user, self.categories)
        categoriestracker.sync_record(self.user, self.category)
        self.user.categoryread_set.get(category=self.category)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

    def test_sync_record_for_category_old_thread_and_reply(self):
        """
        sync_record sets read flag on category with old thread,
        then changes flag to unread when new reply is posted
        """
        self.post_thread(self.user.joined_on - timedelta(days=1))

        add_acl(self.user, self.categories)
        categoriestracker.sync_record(self.user, self.category)
        self.user.categoryread_set.get(category=self.category)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

        self.post_thread(self.user.joined_on + timedelta(days=1))

        categoriestracker.sync_record(self.user, self.category)
        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

    def test_sync_record_for_category_new_thread(self):
        """
        sync_record sets read flag on category with old thread,
        then keeps flag to unread when new reply is posted
        """
        self.post_thread(self.user.joined_on + timedelta(days=1))

        add_acl(self.user, self.categories)
        categoriestracker.sync_record(self.user, self.category)
        self.user.categoryread_set.get(category=self.category)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

        self.post_thread(self.user.joined_on + timedelta(days=1))
        categoriestracker.sync_record(self.user, self.category)
        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

    def test_sync_record_for_category_deleted_threads(self):
        """unread category reverts to read after its emptied"""
        self.post_thread(self.user.joined_on + timedelta(days=1))
        self.post_thread(self.user.joined_on + timedelta(days=1))
        self.post_thread(self.user.joined_on + timedelta(days=1))

        add_acl(self.user, self.categories)
        categoriestracker.sync_record(self.user, self.category)
        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

        self.category.thread_set.all().delete()
        self.category.synchronize()
        self.category.save()

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

    def test_sync_record_for_category_many_threads(self):
        """sync_record sets unread flag on category with many threads"""
        self.post_thread(self.user.joined_on + timedelta(days=1))
        self.post_thread(self.user.joined_on - timedelta(days=1))
        self.post_thread(self.user.joined_on + timedelta(days=1))
        self.post_thread(self.user.joined_on - timedelta(days=1))

        add_acl(self.user, self.categories)
        categoriestracker.sync_record(self.user, self.category)
        self.user.categoryread_set.get(category=self.category)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

        self.post_thread(self.user.joined_on + timedelta(days=1))
        categoriestracker.sync_record(self.user, self.category)
        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

    def test_sync_record_for_category_threads_behind_cutoff(self):
        """
        sync_record sets read flag on category with only thread being behind cutoff
        """
        self.post_thread(timezone.now() - timedelta(days=180))

        read_thread = self.post_thread(timezone.now())

        threadstracker.make_read_aware(self.user, read_thread)
        threadstracker.read_thread(self.user, read_thread, read_thread.last_post)

        category = Category.objects.get(pk=self.category.pk)
        categoriestracker.make_read_aware(self.user, [category])
        self.assertTrue(category.is_read)

    def test_read_leaf_category(self):
        """read_category reads leaf category for user"""
        categoriestracker.read_category(self.user, self.category)

        self.assertTrue(self.user.categoryread_set.get(category=self.category))

    def test_read_root_category(self):
        """read_category reads its subcategories for user"""
        root_category = Category.objects.root_category()
        categoriestracker.read_category(self.user, root_category)

        child_read = self.user.categoryread_set.get(category=self.category)
        self.assertTrue(child_read.last_read_on > timezone.now() - timedelta(seconds=3))

    def test_read_category_prunes_threadreads(self):
        """read_category prunes threadreads in this category"""
        thread = self.post_thread(timezone.now())

        threadstracker.make_read_aware(self.user, thread)
        threadstracker.read_thread(self.user, thread, thread.last_post)

        self.assertTrue(self.user.threadread_set.exists())

        categoriestracker.read_category(self.user, self.category)

        self.assertTrue(self.user.categoryread_set.get(category=self.category))
        self.assertFalse(self.user.threadread_set.exists())


class ThreadsTrackerTests(ReadTrackerTests):
    def setUp(self):
        super(ThreadsTrackerTests, self).setUp()

        self.thread = self.post_thread(timezone.now() - timedelta(days=10))

    def reply_thread(self, is_hidden=False, is_unapproved=False):
        self.post = testutils.reply_thread(
            thread=self.thread,
            is_hidden=is_hidden,
            is_unapproved=is_unapproved,
            posted_on=timezone.now(),
        )
        return self.post

    def test_thread_read_for_guest(self):
        """threads are always read for guests"""
        threadstracker.make_read_aware(self.anon, self.thread)
        self.assertTrue(self.thread.is_read)

        self.reply_thread()
        threadstracker.make_read_aware(self.anon, [self.thread])
        self.assertTrue(self.thread.is_read)

    def test_thread_read_for_user(self):
        """thread is read for user"""
        threadstracker.make_read_aware(self.user, self.thread)
        self.assertTrue(self.thread.is_read)

    def test_thread_replied_unread_for_user(self):
        """replied thread is unread for user"""
        self.reply_thread()

        threadstracker.make_read_aware(self.user, self.thread)
        self.assertFalse(self.thread.is_read)

    def test_thread_read(self):
        """thread read flag is set for user, then its set as unread by reply"""
        self.reply_thread()

        add_acl(self.user, self.categories)
        threadstracker.make_read_aware(self.user, self.thread)
        self.assertFalse(self.thread.is_read)

        threadstracker.read_thread(self.user, self.thread, self.post)
        threadstracker.make_read_aware(self.user, self.thread)
        self.assertTrue(self.thread.is_read)
        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

        self.thread.last_post_on = timezone.now()
        self.thread.save()
        self.category.synchronize()
        self.category.save()

        self.reply_thread()
        threadstracker.make_read_aware(self.user, self.thread)
        self.assertFalse(self.thread.is_read)
        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertFalse(self.category.is_read)

        posts = [post for post in self.thread.post_set.order_by('id')]
        threadstracker.make_posts_read_aware(self.user, self.thread, posts)

        for post in posts[:-1]:
            self.assertTrue(post.is_read)
        self.assertFalse(posts[-1].is_read)

    def test_thread_read_category_cutoff(self):
        """thread read is handled when category cutoff is present"""
        self.reply_thread()

        add_acl(self.user, self.categories)
        threadstracker.make_read_aware(self.user, self.thread)
        self.assertFalse(self.thread.is_read)

        categoriestracker.read_category(self.user, self.category)
        threadstracker.make_read_aware(self.user, self.thread)
        self.assertTrue(self.thread.is_read)

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)

        posts = list(self.thread.post_set.order_by('id'))
        threadstracker.make_posts_read_aware(self.user, self.thread, posts)

        for post in posts:
            self.assertTrue(post.is_read)

        # post reply
        self.reply_thread()

        # test if only last post is unread
        posts = list(self.thread.post_set.order_by('id'))
        threadstracker.make_read_aware(self.user, self.thread)
        threadstracker.make_posts_read_aware(self.user, self.thread, posts)

        for post in posts[:-1]:
            self.assertTrue(post.is_read)
        self.assertTrue(posts[-1].is_new)

        # last post read will change readstate of categories
        threadstracker.make_read_aware(self.user, self.thread)
        threadstracker.read_thread(self.user, self.thread, posts[-1])

        categoriestracker.make_read_aware(self.user, self.categories)
        self.assertTrue(self.category.is_read)
