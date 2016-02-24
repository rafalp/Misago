from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase
from misago.threads import testutils

from misago.readtracker.categoriestracker import make_read_aware


class AuthenticatedTests(AuthenticatedUserTestCase):
    def test_read_all_threads(self):
        """read_all view updates reads cutoff on user model"""
        category = Category.objects.all_categories()[:1][0]
        threads = [testutils.post_thread(category) for t in xrange(10)]

        category = Category.objects.get(id=category.id)
        make_read_aware(self.user, [category])
        self.assertFalse(category.is_read)

        response = self.client.post(reverse('misago:read_all'))
        self.assertEqual(response.status_code, 302)

        category = Category.objects.get(id=category.id)
        user = get_user_model().objects.get(id=self.user.id)

        make_read_aware(user, [category])
        self.assertTrue(category.is_read)

    def test_read_category(self):
        """read_category view updates reads cutoff on category tracker"""
        category = Category.objects.all_categories()[:1][0]
        threads = [testutils.post_thread(category) for t in xrange(10)]

        category = Category.objects.get(id=category.id)
        make_read_aware(self.user, [category])
        self.assertFalse(category.is_read)

        response = self.client.post(reverse('misago:read_category', kwargs={
            'category_id': category.id
        }))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['location'].endswith(category.get_absolute_url()))

        category = Category.objects.get(id=category.id)
        user = get_user_model().objects.get(id=self.user.id)

        make_read_aware(user, [category])
        self.assertTrue(category.is_read)
