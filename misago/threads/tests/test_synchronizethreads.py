from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from misago.forums.models import Forum

from misago.threads import testutils
from misago.threads.management.commands import synchronizethreads


class SynchronizeThreadsTests(TestCase):
    def test_no_threads_sync(self):
        """command works when there are no threads"""
        command = synchronizethreads.Command()

        out = StringIO()
        command.execute(stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, 'No threads were found')

    def test_threads_sync(self):
        """command synchronizes threads"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]

        threads = [testutils.post_thread(forum) for t in xrange(10)]
        for thread in threads:
            [testutils.reply_thread(thread) for r in xrange(thread.pk)]
            thread.replies = 0
            thread.save()

        command = synchronizethreads.Command()

        out = StringIO()
        command.execute(stdout=out)

        for thread in threads:
            db_thread = forum.thread_set.get(id=thread.id)
            self.assertEqual(db_thread.replies, db_thread.pk)

        command_output = out.getvalue().splitlines()[-1].strip()
        self.assertEqual(command_output, 'Synchronized 10 threads')
