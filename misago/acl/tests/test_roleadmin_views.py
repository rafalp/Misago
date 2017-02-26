from django.urls import reverse

from misago.acl.models import Role
from misago.acl.testutils import fake_post_data
from misago.admin.testutils import AdminTestCase


def fake_data(data_dict):
    return fake_post_data(Role(), data_dict)


class RoleAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains user roles link"""
        response = self.client.get(reverse('misago:admin:permissions:users:index'))
        self.assertContains(response, reverse('misago:admin:permissions:users:index'))

    def test_list_view(self):
        """roles list view returns 200"""
        response = self.client.get(reverse('misago:admin:permissions:users:index'))
        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        """new role view has no showstoppers"""
        response = self.client.get(reverse('misago:admin:permissions:users:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:permissions:users:new'), data=fake_data({
                'name': 'Test Role',
            })
        )
        self.assertEqual(response.status_code, 302)

        test_role = Role.objects.get(name='Test Role')
        response = self.client.get(reverse('misago:admin:permissions:users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_role.name)

    def test_edit_view(self):
        """edit role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:users:new'), data=fake_data({
                'name': 'Test Role',
            })
        )

        test_role = Role.objects.get(name='Test Role')

        response = self.client.get(
            reverse('misago:admin:permissions:users:edit', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Role')

        response = self.client.post(
            reverse('misago:admin:permissions:users:edit', kwargs={
                'pk': test_role.pk,
            }),
            data=fake_data({
                'name': 'Top Lel',
            })
        )
        self.assertEqual(response.status_code, 302)

        test_role = Role.objects.get(name='Top Lel')
        response = self.client.get(reverse('misago:admin:permissions:users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_role.name)

    def test_users_view(self):
        """users with this role view has no showstoppers"""
        response = self.client.post(
            reverse('misago:admin:permissions:users:new'), data=fake_data({
                'name': 'Test Role',
            })
        )
        test_role = Role.objects.get(name='Test Role')

        response = self.client.get(
            reverse('misago:admin:permissions:users:users', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        """delete role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:users:new'), data=fake_data({
                'name': 'Test Role',
            })
        )

        test_role = Role.objects.get(name='Test Role')
        response = self.client.post(
            reverse('misago:admin:permissions:users:delete', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertEqual(response.status_code, 302)

        # Get the page twice so no alert is renderered on second request
        self.client.get(reverse('misago:admin:permissions:users:index'))
        response = self.client.get(reverse('misago:admin:permissions:users:index'))
        self.assertNotContains(response, test_role.name)
