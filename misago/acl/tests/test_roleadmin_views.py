from django.core.urlresolvers import reverse
from misago.admin.testutils import AdminTestCase
from misago.acl.models import Role


def fake_data(data_dict):
    data_dict.update({
        'name_changes_allowed': 0,
        'changes_expire': 0,
        'can_use_signature': 0,
        'allow_signature_links': 0,
        'allow_signature_images': 0,
        'can_destroy_user_newer_than': 0,
        'can_destroy_users_with_less_posts_than': 0,
        'can_search_users': 0,
        'can_see_users_emails': 0,
        'can_see_users_ips': 0,
        'can_see_hidden_users': 0,
    })
    return data_dict


class RoleAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains user roles link"""
        response = self.client.get(
            reverse('misago:admin:permissions:users:index'))

        self.assertIn(reverse('misago:admin:permissions:users:index'),
                      response.content)

    def test_list_view(self):
        """roles list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:permissions:users:index'))

        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        """new role view has no showstoppers"""
        response = self.client.get(
            reverse('misago:admin:permissions:users:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_data({'name': 'Test Role'}))
        self.assertEqual(response.status_code, 302)

        test_role = Role.objects.get(name='Test Role')
        response = self.client.get(
            reverse('misago:admin:permissions:users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_role.name, response.content)

    def test_edit_view(self):
        """edit role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_data({'name': 'Test Role'}))

        test_role = Role.objects.get(name='Test Role')

        response = self.client.get(
            reverse('misago:admin:permissions:users:edit',
                    kwargs={'role_id': test_role.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Role', response.content)

        response = self.client.post(
            reverse('misago:admin:permissions:users:edit',
                    kwargs={'role_id': test_role.pk}),
            data=fake_data({'name': 'Top Lel'}))
        self.assertEqual(response.status_code, 302)

        test_role = Role.objects.get(name='Top Lel')
        response = self.client.get(
            reverse('misago:admin:permissions:users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_role.name, response.content)

    def test_delete_view(self):
        """delete role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_data({'name': 'Test Role'}))

        test_role = Role.objects.get(name='Test Role')
        response = self.client.post(
            reverse('misago:admin:permissions:users:delete',
                    kwargs={'role_id': test_role.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:permissions:users:index'))
        response = self.client.get(
            reverse('misago:admin:permissions:users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_role.name not in response.content)
