from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.categories.utils import get_categories_tree
from misago.users.testutils import AuthenticatedUserTestCase


class CategoryViewsTests(AuthenticatedUserTestCase):
    def test_index_renders(self):
        """categories list renders for authenticated"""
        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertIn(node.name, response.content)
            if node.level > 1:
                self.assertIn(node.get_absolute_url(), response.content)

    def test_index_renders_for_guest(self):
        """categories list renders for guest"""
        self.logout_user()

        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertIn(node.name, response.content)
            if node.level > 1:
                self.assertIn(node.get_absolute_url(), response.content)

    def test_index_no_perms_renders(self):
        """categories list renders no visible categories for authenticated"""
        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotIn(node.get_absolute_url(), response.content)

    def test_index_no_perms_renders_for_guest(self):
        """categories list renders no visible categories for guest"""
        self.logout_user()

        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:categories'))

        for node in get_categories_tree(self.user):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotIn(node.get_absolute_url(), response.content)


class CategoryAPIViewsTests(AuthenticatedUserTestCase):
    def test_index_renders(self):
        """api returns categories for authenticated"""
        response = self.client.get(reverse('misago:api:categories'))

        for node in get_categories_tree(self.user):
            self.assertIn(node.name, response.content)
            if node.level > 1:
                self.assertIn(node.get_absolute_url(), response.content)

    def test_index_renders_for_guest(self):
        """api returns categories for guest"""
        self.logout_user()

        response = self.client.get(reverse('misago:api:categories'))

        for node in get_categories_tree(self.user):
            self.assertIn(node.name, response.content)
            if node.level > 1:
                self.assertIn(node.get_absolute_url(), response.content)

    def test_index_no_perms_renders(self):
        """api returns no categories for authenticated"""
        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:api:categories'))

        for node in get_categories_tree(self.user):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotIn(node.get_absolute_url(), response.content)

    def test_index_no_perms_renders_for_guest(self):
        """api returns no categories for guest"""
        self.logout_user()

        override_acl(self.user, {'visible_categories': []})
        response = self.client.get(reverse('misago:api:categories'))

        for node in get_categories_tree(self.user):
            self.assertNotIn(node.name, response.content)
            if node.level > 1:
                self.assertNotIn(node.get_absolute_url(), response.content)
