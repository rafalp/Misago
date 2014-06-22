from django.core.urlresolvers import reverse
from misago.admin.testutils import AdminTestCase
from misago.forums.models import Forum


class ForumAdminViewsTests(AdminTestCase):
    serialized_rollback = True

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
        """move up/down views have no showstoppers"""
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


class ForumAdminDeleteViewTests(AdminTestCase):
    serialized_rollback = True

    def setUp(self):
        super(ForumAdminDeleteViewTests, self).setUp()
        self.root = Forum.objects.root_category()

        """
        Create forums tree for test cases:

        Category A
          + Forum B
            + Subcategory C
            + Subforum D
        Category E
          + Forum F
        """
        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Category A',
                             'new_parent': self.root.pk,
                             'role': 'category',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Category E',
                             'new_parent': self.root.pk,
                             'role': 'category',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })

        self.category_a = Forum.objects.get(slug='category-a')
        self.category_e = Forum.objects.get(slug='category-e')

        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Forum B',
                             'new_parent': self.category_a.pk,
                             'role': 'forum',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        self.forum_b = Forum.objects.get(slug='forum-b')

        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Subcategory C',
                             'new_parent': self.forum_b.pk,
                             'role': 'category',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Subforum D',
                             'new_parent': self.forum_b.pk,
                             'role': 'forum',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })
        self.subforum_d = Forum.objects.get(slug='subforum-d')

        self.client.post(reverse('misago:admin:forums:nodes:new'),
                         data={
                             'name': 'Forum F',
                             'new_parent': self.category_e.pk,
                             'role': 'forum',
                             'prune_started_after': 0,
                             'prune_replied_after': 0,
                         })

    def test_delete_forum_and_threads(self):
        """forum and its contents were deleted"""
        response = self.client.get(
            reverse('misago:admin:forums:nodes:delete',
                    kwargs={'forum_id': self.subforum_d.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:delete',
                    kwargs={'forum_id': self.subforum_d.pk}),
            data={'move_children_to': '', 'move_threads_to': '',})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Forum.objects.all_forums().count(), 5)

    def test_delete_forum_move_threads(self):
        """forum was deleted and its contents were moved"""
        response = self.client.get(
            reverse('misago:admin:forums:nodes:delete',
                    kwargs={'forum_id': self.forum_b.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:delete',
                    kwargs={'forum_id': self.forum_b.pk}),
            data={
                'move_children_to': self.category_e.pk,
                'move_threads_to': self.subforum_d.pk,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Forum.objects.all_forums().count(), 5)

    def test_delete_all(self):
        """forum and its contents were deleted"""
        response = self.client.get(
            reverse('misago:admin:forums:nodes:delete',
                    kwargs={'forum_id': self.forum_b.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:delete',
                    kwargs={'forum_id': self.forum_b.pk}),
            data={'move_children_to': self.root.pk, 'move_threads_to': '',})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Forum.objects.all_forums().count(), 6)

        response = self.client.post(
            reverse('misago:admin:forums:nodes:delete',
                    kwargs={'forum_id': self.forum_b.pk}),
            data={'move_children_to': '', 'move_threads_to': '',})
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Forum.objects.all_forums().count(), 3)
