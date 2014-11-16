from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import UserTestCase, AuthenticatedUserTestCase

from misago.threads import testutils


class AuthenticatedTests(AuthenticatedUserTestCase):
    def override_acl(self):
        new_acl = {
            'can_see': True,
            'can_browse': True,
            'can_see_all_threads': True,
            'can_review_moderated_content': True,
        }

        forums_acl = self.user.acl

        for forum in Forum.objects.all():
            forums_acl['visible_forums'].append(forum.pk)
            forums_acl['moderated_forums'].append(forum.pk)
            forums_acl['forums'][forum.pk] = new_acl

        override_acl(self.user, forums_acl)

    def test_cant_see_threads_list(self):
        """user has no permission to see moderated list"""
        response = self.client.get(reverse('misago:moderated_content'))
        self.assertEqual(response.status_code, 403)
        self.assertIn("review moderated content.", response.content)

    def test_empty_threads_list(self):
        """empty threads list is rendered"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        [testutils.post_thread(forum) for t in xrange(10)]

        self.override_acl();
        response = self.client.get(reverse('misago:moderated_content'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("There are no threads with moderated", response.content)

    def test_filled_threads_list(self):
        """filled threads list is rendered"""
        forum = Forum.objects.all_forums().filter(role="forum")[:1][0]

        threads = []
        for t in xrange(10):
            threads.append(testutils.post_thread(forum, is_moderated=True))

        for t in xrange(10):
            threads.append(testutils.post_thread(forum))
            testutils.reply_thread(threads[-1], is_moderated=True)

        self.override_acl();
        response = self.client.get(reverse('misago:moderated_content'))
        self.assertEqual(response.status_code, 200)
        for thread in threads:
            self.assertIn(thread.get_absolute_url(), response.content)


class AnonymousTests(UserTestCase):
    def test_anon_access_to_view(self):
        """anonymous user has no access to unread threads list"""
        response = self.client.get(reverse('misago:moderated_content'))
        self.assertEqual(response.status_code, 403)
        self.assertIn("sign in to see list", response.content)
