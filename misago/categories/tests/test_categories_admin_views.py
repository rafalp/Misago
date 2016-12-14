from django.urls import reverse

from misago.admin.testutils import AdminTestCase
from misago.threads import testutils
from misago.threads.models import Thread

from ..models import Category


class CategoryAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains categories link"""
        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))

        self.assertContains(response, reverse('misago:admin:categories:nodes:index'))

    def test_list_view(self):
        """categories list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))

        self.assertContains(response, 'First category')

        # Now test that empty categories list contains message
        root = Category.objects.root_category()
        for descendant in root.get_descendants():
            descendant.delete()

        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No categories')

    def test_new_view(self):
        """new category view has no showstoppers"""
        root = Category.objects.root_category()

        response = self.client.get(
            reverse('misago:admin:categories:nodes:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Test Category',
                'description': 'Lorem ipsum dolor met',
                'new_parent': root.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertContains(response, 'Test Category')

        test_category = Category.objects.get(slug='test-category')

        response = self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Test Subcategory',
                'new_parent': test_category.pk,
                'copy_permissions': test_category.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertContains(response, 'Test Subcategory')

    def test_edit_view(self):
        """edit category view has no showstoppers"""
        private_threads = Category.objects.private_threads()
        root = Category.objects.root_category()

        response = self.client.get(
            reverse('misago:admin:categories:nodes:edit', kwargs={
                'pk': private_threads.pk
            }))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:categories:nodes:edit', kwargs={
                'pk': root.pk
            }))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:new'),
            data={
                'name': 'Test Category',
                'description': 'Lorem ipsum dolor met',
                'new_parent': root.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)
        test_category = Category.objects.get(slug='test-category')

        response = self.client.get(
            reverse('misago:admin:categories:nodes:edit', kwargs={
                'pk': test_category.pk
            }))

        self.assertContains(response, 'Test Category')

        response = self.client.post(
            reverse('misago:admin:categories:nodes:edit', kwargs={
                'pk': test_category.pk
            }),
            data={
                'name': 'Test Category Edited',
                'new_parent': root.pk,
                'role': 'category',
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertContains(response, 'Test Category Edited')

    def test_move_views(self):
        """move up/down views have no showstoppers"""
        root = Category.objects.root_category()

        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Category A',
            'new_parent': root.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })

        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Category B',
            'new_parent': root.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })


        category_b = Category.objects.get(slug='category-b')

        response = self.client.post(
            reverse('misago:admin:categories:nodes:up', kwargs={
                'pk': category_b.pk
            }))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:categories:nodes:index'))
        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find(b'Category A')
        position_b = response.content.find(b'Category B')
        self.assertTrue(position_a > position_b)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:up', kwargs={
                'pk': category_b.pk
            }))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:categories:nodes:index'))
        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find(b'Category A')
        position_b = response.content.find(b'Category B')
        self.assertTrue(position_a > position_b)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:down', kwargs={
                'pk': category_b.pk
            }))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:categories:nodes:index'))
        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find(b'Category A')
        position_b = response.content.find(b'Category B')
        self.assertTrue(position_a > position_b)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:down', kwargs={
                'pk': category_b.pk
            }))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:categories:nodes:index'))
        response = self.client.get(
            reverse('misago:admin:categories:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find(b'Category A')
        position_b = response.content.find(b'Category B')
        self.assertTrue(position_a < position_b)


class CategoryAdminDeleteViewTests(AdminTestCase):
    def setUp(self):
        super(CategoryAdminDeleteViewTests, self).setUp()
        self.root = Category.objects.root_category()

        """
        Create categories tree for test cases:

        First category (created by migration)

        Category A
          + Category B
            + Subcategory C
            + Subcategory D

        Category E
          + Category F
        """
        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Category A',
            'new_parent': self.root.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })

        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Category E',
            'new_parent': self.root.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })

        self.category_a = Category.objects.get(slug='category-a')
        self.category_e = Category.objects.get(slug='category-e')

        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Category B',
            'new_parent': self.category_a.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })
        self.category_b = Category.objects.get(slug='category-b')

        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Subcategory C',
            'new_parent': self.category_b.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })
        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Subcategory D',
            'new_parent': self.category_b.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })
        self.category_d = Category.objects.get(slug='subcategory-d')

        self.client.post(reverse('misago:admin:categories:nodes:new'), data={
            'name': 'Category F',
            'new_parent': self.category_e.pk,
            'prune_started_after': 0,
            'prune_replied_after': 0,
        })

    def test_delete_category_move_contents(self):
        """category was deleted and its contents were moved"""
        for i in range(10):
            testutils.post_thread(self.category_b)
        self.assertEqual(Thread.objects.count(), 10)

        response = self.client.get(
            reverse('misago:admin:categories:nodes:delete', kwargs={
                'pk': self.category_b.pk
            }))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:delete', kwargs={
                'pk': self.category_b.pk
            }),
            data={
                'move_children_to': self.category_e.pk,
                'move_threads_to': self.category_d.pk,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.all_categories().count(), 6)
        self.assertEqual(Thread.objects.count(), 10)

    def test_delete_category_and_contents(self):
        """category and its contents were deleted"""
        for i in range(10):
            testutils.post_thread(self.category_b)

        response = self.client.get(
            reverse('misago:admin:categories:nodes:delete', kwargs={
                'pk': self.category_b.pk
            }))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:delete', kwargs={
                'pk': self.category_b.pk
            }),
            data={
                'move_children_to': '',
                'move_threads_to': ''
            })
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Category.objects.all_categories().count(), 4)
        self.assertEqual(Thread.objects.count(), 0)


    def test_delete_leaf_category(self):
        """category was deleted and its contents were moved"""
        for i in range(10):
            testutils.post_thread(self.category_d)
        self.assertEqual(Thread.objects.count(), 10)

        response = self.client.get(
            reverse('misago:admin:categories:nodes:delete', kwargs={
                'pk': self.category_d.pk
            }))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:categories:nodes:delete', kwargs={
                'pk': self.category_d.pk
            }),
            data={
                'move_children_to': '',
                'move_threads_to': '',
            })
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Category.objects.all_categories().count(), 6)
        self.assertEqual(Thread.objects.count(), 0)
