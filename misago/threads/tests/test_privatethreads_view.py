from django.core.urlresolvers import reverse
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import UserTestCase, AuthenticatedUserTestCase

from misago.threads import testutils
from misago.threads.models import ThreadParticipant


class AuthenticatedTests(AuthenticatedUserTestCase):
    def test_empty_threads_list(self):
        """empty threads list is rendered"""
        response = self.client.get(reverse('misago:private_threads'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("You are not participating in any private threads.",
                      response.content)

    def test_cant_use_threads_list(self):
        """user has no permission to use private threads"""
        override_acl(self.user, {'can_use_private_threads': False})

        response = self.client.get(reverse('misago:private_threads'))
        self.assertEqual(response.status_code, 403)
        self.assertIn("use private threads system.",
                      response.content)

    def test_participating_threads_list(self):
        """private threads list displays threads user participates in"""
        override_acl(self.user, {'can_moderate_private_threads': False})

        forum = Forum.objects.private_threads()
        invisible_threads = [testutils.post_thread(forum) for t in xrange(10)]
        visible_threads = [testutils.post_thread(forum) for t in xrange(10)]

        for thread in visible_threads:
            ThreadParticipant.objects.set_owner(thread, self.user)

        # only threads user participates in are displayed
        response = self.client.get(reverse('misago:private_threads'))
        self.assertEqual(response.status_code, 200)

        for thread in invisible_threads:
            self.assertNotIn(thread.get_absolute_url(), response.content)
        for thread in visible_threads:
            self.assertIn(thread.get_absolute_url(), response.content)

    def test_reported_threads_list(self):
        """private threads list displays threads with reports"""
        override_acl(self.user, {'can_moderate_private_threads': True})

        forum = Forum.objects.private_threads()
        invisible_threads = [testutils.post_thread(forum) for t in xrange(10)]
        visible_threads = [testutils.post_thread(forum) for t in xrange(10)]

        for thread in visible_threads:
            thread.has_reported_posts = True
            thread.save()

        # only threads user participates in are displayed
        response = self.client.get(reverse('misago:private_threads'))
        self.assertEqual(response.status_code, 200)

        for thread in invisible_threads:
            self.assertNotIn(thread.get_absolute_url(), response.content)
        for thread in visible_threads:
            self.assertIn(thread.get_absolute_url(), response.content)


class AnonymousTests(UserTestCase):
    def test_anon_access_to_view(self):
        """anonymous user has no access to private threads list"""
        response = self.client.get(reverse('misago:private_threads'))
        self.assertEqual(response.status_code, 403)
        self.assertIn("use private threads system.", response.content)
