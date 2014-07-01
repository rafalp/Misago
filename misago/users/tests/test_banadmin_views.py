from datetime import date

from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase

from misago.users.models import Ban


class BanAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains bans link"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))

        response = self.client.get(response['location'])
        self.assertIn(reverse('misago:admin:users:bans:index'),
                      response.content)

    def test_list_view(self):
        """bans list view returns 200"""
        response = self.client.get(reverse('misago:admin:users:bans:index'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        """new ban view has no showstoppers"""
        response = self.client.get(
            reverse('misago:admin:users:bans:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:bans:new'),
            data={
                'test': '1',
                'banned_value': 'test@test.com',
                'user_message': 'Lorem ipsum dolor met',
                'staff_message': 'Sit amet elit',
                'valid_until': '12-24-%s' % unicode(date.today().year + 1),
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:users:bans:index'))
        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertIn('test@test.com', response.content)

    def test_edit_view(self):
        """edit ban view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:bans:new'),
            data={
                'test': '0',
                'banned_value': 'Admin',
            })

        test_ban = Ban.objects.get(banned_value='admin')
        response = self.client.post(
            reverse('misago:admin:users:bans:edit',
                    kwargs={'ban_id': test_ban.pk}),
            data={
                'test': '1',
                'banned_value': 'test@test.com',
                'user_message': 'Lorem ipsum dolor met',
                'staff_message': 'Sit amet elit',
                'valid_until': '12-24-%s' % unicode(date.today().year + 1),
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:users:bans:index'))
        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertIn('test@test.com', response.content)

    def test_delete_view(self):
        """delete ban view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:bans:new'),
            data={
                'test': '0',
                'banned_value': 'TestBan',
            })

        test_ban = Ban.objects.get(banned_value='testban')

        response = self.client.post(
            reverse('misago:admin:users:bans:delete',
                    kwargs={'ban_id': test_ban.pk}))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:users:bans:index'))
        self.client.get(response['location'])
        response = self.client.get(response['location'])

        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_ban.banned_value not in response.content)
