from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase
from misago.threads import testutils

from misago.readtracker.forumstracker import make_read_aware


class AuthenticatedTests(AuthenticatedUserTestCase):
    def test_read_all_threads(self):
        """read_all view updates reads cutoff on user model"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        threads = [testutils.post_thread(forum) for t in xrange(10)]

        forum = Forum.objects.get(id=forum.id)
        make_read_aware(self.user, [forum])
        self.assertFalse(forum.is_read)

        response = self.client.post(reverse('misago:read_all'))
        self.assertEqual(response.status_code, 302)

        forum = Forum.objects.get(id=forum.id)
        user = get_user_model().objects.get(id=self.user.id)

        make_read_aware(user, [forum])
        self.assertTrue(forum.is_read)

    def test_read_forum(self):
        """read_forum view updates reads cutoff on forum tracker"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        threads = [testutils.post_thread(forum) for t in xrange(10)]

        forum = Forum.objects.get(id=forum.id)
        make_read_aware(self.user, [forum])
        self.assertFalse(forum.is_read)

        response = self.client.post(
            reverse('misago:read_forum', kwargs={'forum_id': forum.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['location'].endswith(forum.get_absolute_url()))

        forum = Forum.objects.get(id=forum.id)
        user = get_user_model().objects.get(id=self.user.id)

        make_read_aware(user, [forum])
        self.assertTrue(forum.is_read)
