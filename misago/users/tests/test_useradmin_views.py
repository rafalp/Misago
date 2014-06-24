from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from misago.admin.testutils import AdminTestCase


class UserAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin index view contains users link"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertIn(reverse('misago:admin:users:accounts:index'),
                      response.content)

    def test_list_view(self):
        """users list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertIn('TestAdmin', response.content)
