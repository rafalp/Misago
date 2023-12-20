from django.urls import reverse

from ...acl.test import patch_user_acl
from ...users.test import AuthenticatedUserTestCase
from ..models import Category


class CategoryViewsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")

    def test_index_renders(self):
        """categories list renders for authenticated"""
        response = self.client.get(reverse("misago:categories"))
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category.get_absolute_url())

    def test_index_renders_for_guest(self):
        """categories list renders for guest"""
        self.logout_user()

        response = self.client.get(reverse("misago:categories"))
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category.get_absolute_url())

    @patch_user_acl({"visible_categories": []})
    def test_index_no_perms_renders(self):
        """categories list renders no visible categories for authenticated"""
        response = self.client.get(reverse("misago:categories"))
        self.assertNotContains(response, self.category.name)
        self.assertNotContains(response, self.category.get_absolute_url())

    @patch_user_acl({"visible_categories": []})
    def test_index_no_perms_renders_for_guest(self):
        """categories list renders no visible categories for guest"""
        self.logout_user()

        response = self.client.get(reverse("misago:categories"))
        self.assertNotContains(response, self.category.name)
        self.assertNotContains(response, self.category.get_absolute_url())
