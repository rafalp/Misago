from django.core.urlresolvers import reverse
from misago.acl.models import Role
from misago.acl.testutils import fake_post_data
from misago.admin.testutils import AdminTestCase
from misago.forums.models import Forum, ForumRole


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

    def test_change_forum_roles_view(self):
        """change forum roles perms view works"""
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_post_data(Role(), {'name': 'Test ForumRole'}))

        test_role = Role.objects.get(name='Test ForumRole')

        root = Forum.objects.root_category()
        for descendant in root.get_descendants():
            descendant.delete()

        self.assertEqual(Forum.objects.count(), 2)
        response = self.client.get(
            reverse('misago:admin:permissions:users:forums',
                    kwargs={'role_id': test_role.pk}))
        self.assertEqual(response.status_code, 302)

        """
        Create forums tree for test cases:

        Category A
          + Forum B
        Category C
          + Forum D
        """
        root = Forum.objects.root_category()
        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Category A',
                             'new_parent': root.pk,
                             'role': 'category',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Category C',
                             'new_parent': root.pk,
                             'role': 'category',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })

        category_a = Forum.objects.get(slug='category-a')
        category_c = Forum.objects.get(slug='category-c')

        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Forum B',
                             'new_parent': category_a.pk,
                             'role': 'forum',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        forum_b = Forum.objects.get(slug='forum-b')

        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Forum D',
                             'new_parent': category_c.pk,
                             'role': 'forum',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        forum_d = Forum.objects.get(slug='forum-d')

        self.assertEqual(Forum.objects.count(), 6)

        # See if form page is rendered
        response = self.client.get(
            reverse('misago:admin:permissions:users:forums',
                    kwargs={'role_id': test_role.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(category_a.name, response.content)
        self.assertIn(forum_b.name, response.content)
        self.assertIn(category_c.name, response.content)
        self.assertIn(forum_d.name, response.content)

        # Set test roles
        self.client.post(
            reverse('misago:admin:permissions:forums:new'),
            data=fake_data({'name': 'Test Comments'}))
        role_comments = ForumRole.objects.get(name='Test Comments')

        self.client.post(
            reverse('misago:admin:permissions:forums:new'),
            data=fake_data({'name': 'Test Full'}))
        role_full = ForumRole.objects.get(name='Test Full')

        # See if form contains those roles
        response = self.client.get(
            reverse('misago:admin:permissions:users:forums',
                    kwargs={'role_id': test_role.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(role_comments.name, response.content)
        self.assertIn(role_full.name, response.content)

        # Assign roles to forums
        response = self.client.post(
            reverse('misago:admin:permissions:users:forums',
                    kwargs={'role_id': test_role.pk}),
            data={
                ('%s-role' % category_a.pk): role_comments.pk,
                ('%s-role' % forum_b.pk): role_comments.pk,
                ('%s-role' % category_c.pk): role_full.pk,
                ('%s-role' % forum_d.pk): role_full.pk,
            })
        self.assertEqual(response.status_code, 302)

        # Check that roles were assigned
        self.assertEqual(
            test_role.forums_acls.get(forum=category_a).forum_role_id,
            role_comments.pk)
        self.assertEqual(
            test_role.forums_acls.get(forum=forum_b).forum_role_id,
            role_comments.pk)
        self.assertEqual(
            test_role.forums_acls.get(forum=category_c).forum_role_id,
            role_full.pk)
        self.assertEqual(
            test_role.forums_acls.get(forum=forum_d).forum_role_id,
            role_full.pk)

    def test_change_role_forums_permissions_view(self):
        """change role forums perms view works"""
        root = Forum.objects.root_category()
        for descendant in root.get_descendants():
            descendant.delete()

        """
        Create forums tree for test cases:

        Category A
          + Forum B
        Category C
          + Forum D
        """
        root = Forum.objects.root_category()
        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Category A',
                             'new_parent': root.pk,
                             'role': 'category',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        test_category = Forum.objects.get(slug='category-a')

        self.assertEqual(Forum.objects.count(), 3)

        """
        Create test roles
        """
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_post_data(Role(), {'name': 'Test Role A'}))
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_post_data(Role(), {'name': 'Test Role B'}))

        test_role_a = Role.objects.get(name='Test Role A')
        test_role_b = Role.objects.get(name='Test Role B')

        self.client.post(
            reverse('misago:admin:permissions:forums:new'),
            data=fake_data({'name': 'Test Comments'}))
        self.client.post(
            reverse('misago:admin:permissions:forums:new'),
            data=fake_data({'name': 'Test Full'}))

        role_comments = ForumRole.objects.get(name='Test Comments')
        role_full = ForumRole.objects.get(name='Test Full')

        """
        Test view itself
        """
        # See if form page is rendered
        response = self.client.get(
            reverse('misago:admin:forums:nodes:permissions',
                    kwargs={'forum_id': test_category.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_category.name, response.content)
        self.assertIn(test_role_a.name, response.content)
        self.assertIn(test_role_b.name, response.content)
        self.assertIn(role_comments.name, response.content)
        self.assertIn(role_full.name, response.content)

        # Assign roles to forums
        response = self.client.post(
            reverse('misago:admin:forums:nodes:permissions',
                    kwargs={'forum_id': test_category.pk}),
            data={
                ('%s-forum_role' % test_role_a.pk): role_full.pk,
                ('%s-forum_role' % test_role_b.pk): role_comments.pk,
            })
        self.assertEqual(response.status_code, 302)

        # Check that roles were assigned
        self.assertEqual(
            test_category.forum_role_set.get(role=test_role_a).forum_role_id,
            role_full.pk)
        self.assertEqual(
            test_category.forum_role_set.get(role=test_role_b).forum_role_id,
            role_comments.pk)
