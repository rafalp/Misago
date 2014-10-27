from django.test import TestCase
from django.utils.six import StringIO

from misago.threads import testutils

from misago.forums.management.commands import synchronizeforums
from misago.forums.models import Forum


class SynchronizeForumsTests(TestCase):
    def test_forums_sync(self):
        """command synchronizes forums"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]

        threads = [testutils.post_thread(forum) for t in xrange(10)]
        for thread in threads:
            [testutils.reply_thread(thread) for r in xrange(5)]

        forum.threads = 0
        forum.posts = 0

        command = synchronizeforums.Command()

        out = StringIO()
        command.execute(stdout=out)

        forum = Forum.objects.get(id=forum.id)
        self.assertEqual(forum.threads, 10)
        self.assertEqual(forum.posts, 60)

        command_output = out.getvalue().splitlines()[-1].strip()
        self.assertEqual(command_output, 'Synchronized 5 forums')
