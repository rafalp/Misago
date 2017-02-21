from django.urls import reverse

from misago.acl.models import Role
from misago.acl.testutils import fake_post_data
from misago.admin.testutils import AdminTestCase
from misago.categories.models import Category, CategoryRole


def fake_data(data_dict):
    return fake_post_data(CategoryRole(), data_dict)


class CategoryRoleAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains category roles link"""
        response = self.client.get(reverse('misago:admin:permissions:categories:index'))

        self.assertContains(response, reverse('misago:admin:permissions:categories:index'))

    def test_list_view(self):
        """roles list view returns 200"""
        response = self.client.get(reverse('misago:admin:permissions:categories:index'))

        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        """new role view has no showstoppers"""
        response = self.client.get(reverse('misago:admin:permissions:categories:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:permissions:categories:new'),
            data=fake_data({
                'name': 'Test CategoryRole',
            }),
        )
        self.assertEqual(response.status_code, 302)

        test_role = CategoryRole.objects.get(name='Test CategoryRole')
        response = self.client.get(reverse('misago:admin:permissions:categories:index'))
        self.assertContains(response, test_role.name)

    def test_edit_view(self):
        """edit role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:categories:new'),
            data=fake_data({
                'name': 'Test CategoryRole',
            }),
        )

        test_role = CategoryRole.objects.get(name='Test CategoryRole')

        response = self.client.get(
            reverse('misago:admin:permissions:categories:edit', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertContains(response, 'Test CategoryRole')

        response = self.client.post(
            reverse('misago:admin:permissions:categories:edit', kwargs={
                'pk': test_role.pk,
            }),
            data=fake_data({
                'name': 'Top Lel',
            }),
        )
        self.assertEqual(response.status_code, 302)

        test_role = CategoryRole.objects.get(name='Top Lel')
        response = self.client.get(reverse('misago:admin:permissions:categories:index'))
        self.assertContains(response, test_role.name)

    def test_delete_view(self):
        """delete role view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:permissions:categories:new'),
            data=fake_data({
                'name': 'Test CategoryRole',
            }),
        )

        test_role = CategoryRole.objects.get(name='Test CategoryRole')
        response = self.client.post(
            reverse('misago:admin:permissions:categories:delete', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:permissions:categories:index'))
        response = self.client.get(reverse('misago:admin:permissions:categories:index'))
        self.assertNotContains(response, test_role.name)

    def test_change_category_roles_view(self):
        """change category roles perms view works"""
        root = Category.objects.root_category()
        for descendant in root.get_descendants():
            descendant.delete()
        """
        Create categories tree for test cases:

        Category A
          + Category B
        Category C
          + Category D
        """
        root = Category.objects.root_category()
        self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Category A',
                'new_parent': root.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            },
        )
        test_category = Category.objects.get(slug='category-a')

        self.assertEqual(Category.objects.count(), 3)
        """
        Create test roles
        """
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_post_data(Role(), {'name': 'Test Role A'})
        )
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_post_data(Role(), {'name': 'Test Role B'})
        )

        test_role_a = Role.objects.get(name='Test Role A')
        test_role_b = Role.objects.get(name='Test Role B')

        self.client.post(
            reverse('misago:admin:permissions:categories:new'),
            data=fake_data({
                'name': 'Test Comments',
            }),
        )
        self.client.post(
            reverse('misago:admin:permissions:categories:new'),
            data=fake_data({
                'name': 'Test Full',
            }),
        )

        role_comments = CategoryRole.objects.get(name='Test Comments')
        role_full = CategoryRole.objects.get(name='Test Full')
        """
        Test view itself
        """
        # See if form page is rendered
        response = self.client.get(
            reverse(
                'misago:admin:categories:nodes:permissions', kwargs={
                    'pk': test_category.pk,
                }
            )
        )
        self.assertContains(response, test_category.name)
        self.assertContains(response, test_role_a.name)
        self.assertContains(response, test_role_b.name)
        self.assertContains(response, role_comments.name)
        self.assertContains(response, role_full.name)

        # Assign roles to categories
        response = self.client.post(
            reverse(
                'misago:admin:categories:nodes:permissions', kwargs={
                    'pk': test_category.pk,
                }
            ),
            data={
                ('%s-category_role' % test_role_a.pk): role_full.pk,
                ('%s-category_role' % test_role_b.pk): role_comments.pk,
            },
        )
        self.assertEqual(response.status_code, 302)

        # Check that roles were assigned
        category_role_set = test_category.category_role_set
        self.assertEqual(category_role_set.get(role=test_role_a).category_role_id, role_full.pk)
        self.assertEqual(
            category_role_set.get(role=test_role_b).category_role_id, role_comments.pk
        )

    def test_change_role_categories_permissions_view(self):
        """change role categories perms view works"""
        self.client.post(
            reverse('misago:admin:permissions:users:new'),
            data=fake_post_data(Role(), {'name': 'Test CategoryRole'})
        )

        test_role = Role.objects.get(name='Test CategoryRole')

        root = Category.objects.root_category()
        for descendant in root.get_descendants():
            descendant.delete()

        self.assertEqual(Category.objects.count(), 2)
        response = self.client.get(
            reverse('misago:admin:permissions:users:categories', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertEqual(response.status_code, 302)
        """
        Create categories tree for test cases:

        Category A
          + Category B
        Category C
          + Category D
        """
        root = Category.objects.root_category()
        self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Category A',
                'new_parent': root.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            },
        )
        self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Category C',
                'new_parent': root.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            },
        )

        category_a = Category.objects.get(slug='category-a')
        category_c = Category.objects.get(slug='category-c')

        self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Category B',
                'new_parent': category_a.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            },
        )
        category_b = Category.objects.get(slug='category-b')

        self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Category D',
                'new_parent': category_c.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            },
        )
        category_d = Category.objects.get(slug='category-d')

        self.assertEqual(Category.objects.count(), 6)

        # See if form page is rendered
        response = self.client.get(
            reverse('misago:admin:permissions:users:categories', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertContains(response, category_a.name)
        self.assertContains(response, category_b.name)
        self.assertContains(response, category_c.name)
        self.assertContains(response, category_d.name)

        # Set test roles
        self.client.post(
            reverse('misago:admin:permissions:categories:new'),
            data=fake_data({
                'name': 'Test Comments',
            }),
        )
        role_comments = CategoryRole.objects.get(name='Test Comments')

        self.client.post(
            reverse('misago:admin:permissions:categories:new'),
            data=fake_data({
                'name': 'Test Full',
            }),
        )
        role_full = CategoryRole.objects.get(name='Test Full')

        # See if form contains those roles
        response = self.client.get(
            reverse('misago:admin:permissions:users:categories', kwargs={
                'pk': test_role.pk,
            })
        )
        self.assertContains(response, role_comments.name)
        self.assertContains(response, role_full.name)

        # Assign roles to categories
        response = self.client.post(
            reverse('misago:admin:permissions:users:categories', kwargs={
                'pk': test_role.pk,
            }),
            data={
                ('%s-role' % category_a.pk): role_comments.pk,
                ('%s-role' % category_b.pk): role_comments.pk,
                ('%s-role' % category_c.pk): role_full.pk,
                ('%s-role' % category_d.pk): role_full.pk,
            },
        )
        self.assertEqual(response.status_code, 302)

        # Check that roles were assigned
        categories_acls = test_role.categories_acls
        self.assertEqual(
            categories_acls.get(category=category_a).category_role_id, role_comments.pk
        )
        self.assertEqual(
            categories_acls.get(category=category_b).category_role_id, role_comments.pk
        )
        self.assertEqual(categories_acls.get(category=category_c).category_role_id, role_full.pk)
        self.assertEqual(categories_acls.get(category=category_d).category_role_id, role_full.pk)
