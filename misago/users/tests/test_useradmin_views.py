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

    def test_list_search(self):
        """users list is searchable"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))
        self.assertEqual(response.status_code, 302)

        link_base = response['location']
        response = self.client.get(link_base)
        self.assertEqual(response.status_code, 200)

        User = get_user_model()
        user_a = User.objects.create_user('Tyrael', 't123@test.com', 'pass123')
        user_b = User.objects.create_user('Tyrion', 't321@test.com', 'pass123')

        # Search both
        response = self.client.get(link_base + '&username_slug=tyr')
        self.assertEqual(response.status_code, 200)
        self.assertIn(user_a.username, response.content)
        self.assertIn(user_b.username, response.content)

        # Search tyrion
        response = self.client.get(link_base + '&username_slug=tyrion')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_a.username in response.content)
        self.assertIn(user_b.username, response.content)

        # Search tyrael
        response = self.client.get(link_base + '&email=t123@test.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn(user_a.username, response.content)
        self.assertFalse(user_b.username in response.content)
