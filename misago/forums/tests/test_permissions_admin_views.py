from django.core.urlresolvers import reverse
from misago.acl import get_change_permissions_forms
from misago.acl.testutils import fake_post_data
from misago.admin.testutils import AdminTestCase
from misago.forums.models import ForumRole


def fake_data(data_dict):
    return fake_post_data(ForumRole(), data_dict)


class ForumRoleAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains forum roles link"""
        response = self.client.get(
            reverse('misago:admin:permissions:forums:index'))

        self.assertIn(reverse('misago:admin:permissions:forums:index'),
                      response.content)

    def test_list_view(self):
        """roles list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:permissions:forums:index'))

        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        """new role view has no showstoppers"""
        response = self.client.get(
            reverse('misago:admin:permissions:forums:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:permissions:forums:new'),
            data=fake_data({'name': 'Test ForumRole'}))
        self.assertEqual(response.status_code, 302)

        test_role = ForumRole.objects.get(name='Test ForumRole')
        response = self.client.get(
            reverse('misago:admin:permissions:forums:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_role.name, response.content)

    def test_edit_view(self):
        """edit role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:forums:new'),
            data=fake_data({'name': 'Test ForumRole'}))

        test_role = ForumRole.objects.get(name='Test ForumRole')

        response = self.client.get(
            reverse('misago:admin:permissions:forums:edit',
                    kwargs={'role_id': test_role.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test ForumRole', response.content)

        response = self.client.post(
            reverse('misago:admin:permissions:forums:edit',
                    kwargs={'role_id': test_role.pk}),
            data=fake_data({'name': 'Top Lel'}))
        self.assertEqual(response.status_code, 302)

        test_role = ForumRole.objects.get(name='Top Lel')
        response = self.client.get(
            reverse('misago:admin:permissions:forums:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_role.name, response.content)

    def test_delete_view(self):
        """delete role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:forums:new'),
            data=fake_data({'name': 'Test ForumRole'}))

        test_role = ForumRole.objects.get(name='Test ForumRole')
        response = self.client.post(
            reverse('misago:admin:permissions:forums:delete',
                    kwargs={'role_id': test_role.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:permissions:forums:index'))
        response = self.client.get(
            reverse('misago:admin:permissions:forums:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(test_role.name not in response.content)
