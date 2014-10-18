from django.core.urlresolvers import reverse
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.testutils import post_thread, reply_thread


class ThreadViewTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadViewTests, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
