from django.core.urlresolvers import reverse
from misago.admin.testutils import AdminTestCase
from misago.forums.models import Forum


class ForumAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains forums link"""
        response = self.client.get(reverse('misago:admin:forums:nodes:index'))

        self.assertIn(reverse('misago:admin:forums:nodes:index'),
                      response.content)

    def test_list_view(self):
        """forums list view returns 200"""
        response = self.client.get(reverse('misago:admin:forums:nodes:index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('No forums', response.content)

    def test_new_view(self):
        """new forum view has no showstoppers"""
        root = Forum.objects.root_category()

        response = self.client.get(
            reverse('misago:admin:forums:nodes:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:new'),
            data={
                'name': 'Test Category',
                'description': 'Lorem ipsum dolor met',
                'new_parent': root.pk,
                'role': 'category',
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:forums:nodes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Category', response.content)

        test_category = Forum.objects.all_forums().get(slug='test-category')

        response = self.client.post(
            reverse('misago:admin:forums:nodes:new'),
            data={
                'name': 'Test Forum',
                'new_parent': test_category.pk,
                'role': 'forum',
                'copy_permissions': test_category.pk,
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:forums:nodes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Forum', response.content)

    def test_edit_view(self):
        """edit forum view has no showstoppers"""
        private_threads = Forum.objects.private_threads()
        root = Forum.objects.root_category()

        response = self.client.get(
            reverse('misago:admin:forums:nodes:edit',
                    kwargs={'forum_id': private_threads.pk}))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:forums:nodes:edit',
                    kwargs={'forum_id': root.pk}))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:new'),
            data={
                'name': 'Test Category',
                'description': 'Lorem ipsum dolor met',
                'new_parent': root.pk,
                'role': 'category',
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)
        test_category = Forum.objects.all_forums().get(slug='test-category')

        response = self.client.get(
            reverse('misago:admin:forums:nodes:edit',
                    kwargs={'forum_id': test_category.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Category', response.content)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:edit',
                    kwargs={'forum_id': test_category.pk}),
            data={
                'name': 'Test Category Edited',
                'new_parent': root.pk,
                'role': 'category',
                'prune_started_after': 0,
                'prune_replied_after': 0,
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:forums:nodes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Category Edited', response.content)

    def test_move_views(self):
        """move up view has no showstoppers"""
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
                             'name': 'Category B',
                             'new_parent': root.pk,
                             'role': 'category',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })

        category_a = Forum.objects.get(slug='category-a')
        category_b = Forum.objects.get(slug='category-b')

        response = self.client.post(
            reverse('misago:admin:forums:nodes:up',
                    kwargs={'forum_id': category_b.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:forums:nodes:index'))
        response = self.client.get(reverse('misago:admin:forums:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find('Category A')
        position_b = response.content.find('Category B')
        self.assertTrue(position_a > position_b)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:up',
                    kwargs={'forum_id': category_b.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:forums:nodes:index'))
        response = self.client.get(reverse('misago:admin:forums:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find('Category A')
        position_b = response.content.find('Category B')
        self.assertTrue(position_a > position_b)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:down',
                    kwargs={'forum_id': category_b.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:forums:nodes:index'))
        response = self.client.get(reverse('misago:admin:forums:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find('Category A')
        position_b = response.content.find('Category B')
        self.assertTrue(position_a < position_b)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:down',
                    kwargs={'forum_id': category_b.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:forums:nodes:index'))
        response = self.client.get(reverse('misago:admin:forums:nodes:index'))
        self.assertEqual(response.status_code, 200)
        position_a = response.content.find('Category A')
        position_b = response.content.find('Category B')
        self.assertTrue(position_a < position_b)
