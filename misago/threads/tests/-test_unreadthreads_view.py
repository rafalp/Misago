from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.categories.models import Category
from misago.users.testutils import UserTestCase, AuthenticatedUserTestCase

from misago.threads import testutils


class AuthenticatedTests(AuthenticatedUserTestCase):
    def test_empty_threads_list(self):
        """empty threads list is rendered"""
        response = self.client.get(reverse('misago:unread_threads'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("There are no threads with unread", response.content)

    def test_filled_threads_list(self):
        """filled threads list is rendered"""
        category = Category.objects.all_categories().filter(role='forum')[:1][0]
        threads = [testutils.post_thread(category) for t in xrange(10)]

        # only unread tracker threads are shown on unread list
        response = self.client.get(reverse('misago:unread_threads'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("There are no threads with unread", response.content)

        # we'll read and reply to first five threads
        for thread in threads[5:]:
            response = self.client.get(thread.get_absolute_url())
            testutils.reply_thread(thread, posted_on=timezone.now())

        # assert that replied threads show on list
        response = self.client.get(reverse('misago:unread_threads'))
        self.assertEqual(response.status_code, 200)
        for thread in threads[5:]:
            self.assertIn(thread.get_absolute_url(), response.content)
        for thread in threads[:5]:
            self.assertNotIn(thread.get_absolute_url(), response.content)

        # clear list
        response = self.client.post(reverse('misago:clear_unread_threads'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertIn("There are no threads with unread", response.content)


class AnonymousTests(UserTestCase):
    def test_anon_access_to_view(self):
        """anonymous user has no access to unread threads list"""
        response = self.client.get(reverse('misago:unread_threads'))
        self.assertEqual(response.status_code, 403)
        self.assertIn(_("You have to sign in to see your list of "
                        "threads with unread replies."),
                      response.content)
