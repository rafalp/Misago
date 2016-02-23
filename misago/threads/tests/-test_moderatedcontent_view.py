from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from misago.acl.testutils import override_acl
from misago.categories.models import Category
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

        categories_acl = self.user.acl

        for category in Category.objects.all():
            categories_acl['visible_categories'].append(category.pk)
            categories_acl['can_review_moderated_content'].append(category.pk)
            categories_acl['categories'][category.pk] = new_acl

        override_acl(self.user, categories_acl)

    def test_cant_see_threads_list(self):
        """user has no permission to see moderated list"""
        response = self.client.get(reverse('misago:moderated_content'))
        self.assertEqual(response.status_code, 403)
        self.assertIn("review moderated content.", response.content)

    def test_empty_threads_list(self):
        """empty threads list is rendered"""
        category = Category.objects.all_categories().filter(role="category")[:1][0]
        [testutils.post_thread(category) for t in xrange(10)]

        self.override_acl();
        response = self.client.get(reverse('misago:moderated_content'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("There are no threads with moderated", response.content)

    def test_filled_threads_list(self):
        """filled threads list is rendered"""
        category = Category.objects.all_categories().filter(role="category")[:1][0]

        threads = []
        for t in xrange(10):
            threads.append(testutils.post_thread(category, is_moderated=True))

        for t in xrange(10):
            threads.append(testutils.post_thread(category))
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
