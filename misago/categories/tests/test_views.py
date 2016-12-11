from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase

from ..models import Category
from ..utils import get_categories_tree


class CategoryViewsTests(AuthenticatedUserTestCase):
    def test_index_renders(self):
        """categories list renders for authenticated"""
        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertContains(response, node.name)
            if node.level > 1:
                self.assertContains(response, node.get_absolute_url())

    def test_index_renders_for_guest(self):
        """categories list renders for guest"""
        self.logout_user()

        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertContains(response, node.name)
            if node.level > 1:
                self.assertContains(response, node.get_absolute_url())

    def test_index_no_perms_renders(self):
        """categories list renders no visible categories for authenticated"""
        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotContains(response, node.get_absolute_url())

    def test_index_no_perms_renders_for_guest(self):
        """categories list renders no visible categories for guest"""
        self.logout_user()

        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotContains(response, node.get_absolute_url())


class CategoryAPIViewsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(CategoryAPIViewsTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.api_link = reverse('misago:api:category-read', kwargs={
            'pk': self.category.pk
        })

    def test_list_renders(self):
        """api returns categories for authenticated"""
        response = self.client.get(reverse('misago:api:category-list'))

        for node in get_categories_tree(self.user):
            self.assertContains(response, node.name)
            if node.level > 1:
                self.assertNotContains(response, node.get_absolute_url())

    def test_list_renders_for_guest(self):
        """api returns categories for guest"""
        self.logout_user()

        response = self.client.get(reverse('misago:api:category-list'))

        for node in get_categories_tree(self.user):
            self.assertContains(response, node.name)
            if node.level > 1:
                self.assertNotContains(response, node.get_absolute_url())

    def test_list_no_perms_renders(self):
        """api returns no categories for authenticated"""
        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:api:category-list'))

        for node in get_categories_tree(self.user):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotContains(response, node.get_absolute_url())

    def test_list_no_perms_renders_for_guest(self):
        """api returns no categories for guest"""
        self.logout_user()

        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:api:category-list'))

        for node in get_categories_tree(self.user):
            self.assertNotContains(response, node.name)
            if node.level > 1:
                self.assertNotContains(response, node.get_absolute_url())

    def test_read_category_guest(self):
        """category read api validates that user is authenticated"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertContains(response, "This action is not available to guests.", status_code=403)

    def test_read_invalid_category(self):
        """category read api validates category id"""
        api_link = reverse('misago:api:category-read', kwargs={
            'pk': 'abcd'
        })

        response = self.client.post(api_link)
        self.assertEqual(response.status_code, 404)

    def test_read_nonexistant_category(self):
        """category read api validates category visibility"""
        api_link = reverse('misago:api:category-read', kwargs={
            'pk': self.category.pk * 2
        })

        response = self.client.post(api_link)
        self.assertEqual(response.status_code, 404)

    def test_read_category_no_permission(self):
        """category read api validates category permission"""
        override_acl(self.user, {'visible_categories': []})

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_read_category(self):
        """category read api reads category"""
        # clean reads
        self.user.categoryread_set.all().delete()
        self.assertEqual(self.user.categoryread_set.count(), 0)

        # call api
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        # assert that new read was created
        self.assertEqual(self.user.categoryread_set.count(), 1)

        read = self.user.categoryread_set.order_by('id').last()
        self.assertEqual(read.category_id, self.category.id)
        self.assertTrue(read.last_read_on > timezone.now() - timedelta(seconds=3))

    def test_read_root_category(self):
        """category read api reads root category"""
        category = Category.objects.root_category()
        api_link = reverse('misago:api:category-read', kwargs={
            'pk': category.pk
        })

        # clean reads
        self.user.categoryread_set.all().delete()
        self.assertEqual(self.user.categoryread_set.count(), 0)

        # call api
        response = self.client.post(api_link)
        self.assertEqual(response.status_code, 200)

        # assert that new read for subcategory was created
        self.assertEqual(self.user.categoryread_set.count(), 1)

        read = self.user.categoryread_set.order_by('id').last()
        self.assertEqual(read.category_id, self.category.id)
        self.assertTrue(read.last_read_on > timezone.now() - timedelta(seconds=3))
