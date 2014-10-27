from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from misago.threads import testutils

from misago.forums.management.commands import pruneforums
from misago.forums.models import Forum


class PruneForumsTests(TestCase):
    def test_forum_prune_by_start_date(self):
        """command prunes forum content based on start date"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]

        forum.prune_started_after = 20
        forum.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        posted_on = timezone.now()
        for t in xrange(10):
            thread = testutils.post_thread(forum, started_on=started_on)
            testutils.reply_thread(thread, posted_on=posted_on)

        # post recent threads that will be preserved
        threads = [testutils.post_thread(forum) for t in xrange(10)]

        forum.synchronize()
        self.assertEqual(forum.threads, 20)
        self.assertEqual(forum.posts, 30)

        # run command
        command = pruneforums.Command()

        out = StringIO()
        command.execute(stdout=out)

        forum.synchronize()
        self.assertEqual(forum.threads, 10)
        self.assertEqual(forum.posts, 10)

        for thread in threads:
            forum.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, 'Forums were pruned')

    def test_forum_prune_by_last_reply(self):
        """command prunes forum content based on last reply date"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]

        forum.prune_replied_after = 20
        forum.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        for t in xrange(10):
            thread = testutils.post_thread(forum, started_on=started_on)
            testutils.reply_thread(thread)

        # post recent threads that will be preserved
        threads = [testutils.post_thread(forum) for t in xrange(10)]

        forum.synchronize()
        self.assertEqual(forum.threads, 20)
        self.assertEqual(forum.posts, 30)

        # run command
        command = pruneforums.Command()

        out = StringIO()
        command.execute(stdout=out)

        forum.synchronize()
        self.assertEqual(forum.threads, 10)
        self.assertEqual(forum.posts, 10)

        for thread in threads:
            forum.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, 'Forums were pruned')

    def test_forum_archive_by_start_date(self):
        """command archives forum content based on start date"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        archive = Forum.objects.all_forums().filter(role="category")[:1][0]

        forum.prune_started_after = 20
        forum.archive_pruned_in = archive
        forum.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        posted_on = timezone.now()
        for t in xrange(10):
            thread = testutils.post_thread(forum, started_on=started_on)
            testutils.reply_thread(thread, posted_on=posted_on)

        # post recent threads that will be preserved
        threads = [testutils.post_thread(forum) for t in xrange(10)]

        forum.synchronize()
        self.assertEqual(forum.threads, 20)
        self.assertEqual(forum.posts, 30)

        # run command
        command = pruneforums.Command()

        out = StringIO()
        command.execute(stdout=out)

        forum.synchronize()
        self.assertEqual(forum.threads, 10)
        self.assertEqual(forum.posts, 10)

        archive.synchronize()
        self.assertEqual(archive.threads, 10)
        self.assertEqual(archive.posts, 20)

        for thread in threads:
            forum.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, 'Forums were pruned')

    def test_forum_archive_by_last_reply(self):
        """command archives forum content based on last reply date"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        archive = Forum.objects.all_forums().filter(role="category")[:1][0]

        forum.prune_replied_after = 20
        forum.archive_pruned_in = archive
        forum.save()

        # post old threads with recent replies
        started_on = timezone.now() - timedelta(days=30)
        for t in xrange(10):
            thread = testutils.post_thread(forum, started_on=started_on)
            testutils.reply_thread(thread)

        # post recent threads that will be preserved
        threads = [testutils.post_thread(forum) for t in xrange(10)]

        forum.synchronize()
        self.assertEqual(forum.threads, 20)
        self.assertEqual(forum.posts, 30)

        # run command
        command = pruneforums.Command()

        out = StringIO()
        command.execute(stdout=out)

        forum.synchronize()
        self.assertEqual(forum.threads, 10)
        self.assertEqual(forum.posts, 10)

        archive.synchronize()
        self.assertEqual(archive.threads, 10)
        self.assertEqual(archive.posts, 20)

        for thread in threads:
            forum.thread_set.get(id=thread.id)

        command_output = out.getvalue().strip()
        self.assertEqual(command_output, 'Forums were pruned')
