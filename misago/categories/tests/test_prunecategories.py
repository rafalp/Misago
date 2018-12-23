from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from ...threads import test
from ..management.commands import prunecategories
from ..models import Category


class PruneCategoriesTests(TestCase):
    def test_category_prune_by_start_date(self):
        """command prunes category content based on start date"""
        category = Category.objects.all_categories()[:1][0]

        category.prune_started_after = 20
        category.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        posted_on = timezone.now()
        for _ in range(10):
            thread = test.post_thread(category, started_on=started_on)
            test.reply_thread(thread, posted_on=posted_on)

        # post recent threads that will be preserved
        threads = [test.post_thread(category) for _ in range(10)]

        category.synchronize()
        self.assertEqual(category.threads, 20)
        self.assertEqual(category.posts, 30)

        # run command
        command = prunecategories.Command()

        out = StringIO()
        call_command(command, stdout=out)

        category.synchronize()
        self.assertEqual(category.threads, 10)
        self.assertEqual(category.posts, 10)

        for thread in threads:
            category.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, "Categories were pruned")

    def test_category_prune_by_last_reply(self):
        """command prunes category content based on last reply date"""
        category = Category.objects.all_categories()[:1][0]

        category.prune_replied_after = 20
        category.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        for _ in range(10):
            thread = test.post_thread(category, started_on=started_on)
            test.reply_thread(thread)

        # post recent threads that will be preserved
        threads = [test.post_thread(category) for _ in range(10)]

        category.synchronize()
        self.assertEqual(category.threads, 20)
        self.assertEqual(category.posts, 30)

        # run command
        command = prunecategories.Command()

        out = StringIO()
        call_command(command, stdout=out)

        category.synchronize()
        self.assertEqual(category.threads, 10)
        self.assertEqual(category.posts, 10)

        for thread in threads:
            category.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, "Categories were pruned")

    def test_category_archive_by_start_date(self):
        """command archives category content based on start date"""
        category = Category.objects.all_categories()[:1][0]
        archive = Category.objects.create(
            lft=7, rght=8, tree_id=2, level=0, name="Archive", slug="archive"
        )

        category.prune_started_after = 20
        category.archive_pruned_in = archive
        category.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        posted_on = timezone.now()
        for _ in range(10):
            thread = test.post_thread(category, started_on=started_on)
            test.reply_thread(thread, posted_on=posted_on)

        # post recent threads that will be preserved
        threads = [test.post_thread(category) for _ in range(10)]

        category.synchronize()
        self.assertEqual(category.threads, 20)
        self.assertEqual(category.posts, 30)

        # run command
        command = prunecategories.Command()

        out = StringIO()
        call_command(command, stdout=out)

        category.synchronize()
        self.assertEqual(category.threads, 10)
        self.assertEqual(category.posts, 10)

        archive.synchronize()
        self.assertEqual(archive.threads, 10)
        self.assertEqual(archive.posts, 20)

        for thread in threads:
            category.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, "Categories were pruned")

    def test_category_archive_by_last_reply(self):
        """command archives category content based on last reply date"""
        category = Category.objects.all_categories()[:1][0]
        archive = Category.objects.create(
            lft=7, rght=8, tree_id=2, level=0, name="Archive", slug="archive"
        )

        category.prune_replied_after = 20
        category.archive_pruned_in = archive
        category.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        for _ in range(10):
            thread = test.post_thread(category, started_on=started_on)
            test.reply_thread(thread)

        # post recent threads that will be preserved
        threads = [test.post_thread(category) for _ in range(10)]

        category.synchronize()
        self.assertEqual(category.threads, 20)
        self.assertEqual(category.posts, 30)

        # run command
        command = prunecategories.Command()

        out = StringIO()
        call_command(command, stdout=out)

        category.synchronize()
        self.assertEqual(category.threads, 10)
        self.assertEqual(category.posts, 10)

        archive.synchronize()
        self.assertEqual(archive.threads, 10)
        self.assertEqual(archive.posts, 20)

        for thread in threads:
            category.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, "Categories were pruned")
