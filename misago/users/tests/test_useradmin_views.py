from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse

from misago.acl.models import Role
from misago.admin.testutils import AdminTestCase

from misago.users.models import Rank


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
        response = self.client.get(link_base + '&username=tyr')
        self.assertEqual(response.status_code, 200)
        self.assertIn(user_a.username, response.content)
        self.assertIn(user_b.username, response.content)

        # Search tyrion
        response = self.client.get(link_base + '&username=tyrion')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_a.username in response.content)
        self.assertIn(user_b.username, response.content)

        # Search tyrael
        response = self.client.get(link_base + '&email=t123@test.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn(user_a.username, response.content)
        self.assertFalse(user_b.username in response.content)

    def test_new_view(self):
        """new user view creates account"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:new'))
        self.assertEqual(response.status_code, 200)

        default_rank = Rank.objects.get_default()
        authenticated_role = Role.objects.get(special_role='authenticated')

        response = self.client.post(reverse('misago:admin:users:accounts:new'),
            data={
                'username': 'Bawww',
                'rank': unicode(default_rank.pk),
                'roles': unicode(authenticated_role.pk),
                'email': 'reg@stered.com',
                'new_password': 'pass123',
                'staff_level': '0'
            })
        self.assertEqual(response.status_code, 302)

        User = get_user_model()
        User.objects.get_by_username('Bawww')

    def test_edit_view(self):
        """edit user view changes account"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123')
        test_link = reverse('misago:admin:users:accounts:edit',
                            kwargs={'user_id': test_user.pk})

        response = self.client.get(test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(test_link,
            data={
                'username': 'Bawww',
                'rank': unicode(test_user.rank_id),
                'roles': unicode(test_user.roles.all()[0].pk),
                'email': 'reg@stered.com',
                'new_password': 'pass123',
                'staff_level': '0',
                'signature': 'Hello world!',
                'is_signature_banned': '1',
                'signature_ban_staff_message': 'Staff message',
                'signature_ban_user_message': 'User message',
            })
        self.assertEqual(response.status_code, 302)

        User.objects.get_by_username('Bawww')
        User.objects.get_by_email('reg@stered.com')

    def test_activate_view(self):
        """activate user view activates account"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'pass123',
                                             requires_activation=1)

        test_link = reverse('misago:admin:users:accounts:activate',
                            kwargs={'user_id': test_user.pk})
        response = self.client.post(test_link)
        self.assertEqual(response.status_code, 302)

        self.assertIn("has been activated", mail.outbox[0].subject)

        test_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 0)
