# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase


class ValidatePostTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ValidatePostTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.api_link = reverse('misago:api:thread-list')

    def test_title_validation(self):
        """validate_post tests title"""
        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': 'Check our l33t CaSiNo!',
                'post': 'Lorem ipsum dolor met!',
            }
        )
        self.assertContains(response, "Don't discuss gambling!", status_code=400)

        # clean title passes validation
        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': 'Check our l33t place!',
                'post': 'Lorem ipsum dolor met!',
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_post_validation(self):
        """validate_post tests post content"""
        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': 'Lorem ipsum dolor met!',
                'post': 'Check our l33t CaSiNo!',
            }
        )
        self.assertContains(response, "Don't discuss gambling!", status_code=400)

        # clean post passes validation
        response = self.client.post(
            self.api_link,
            data={
                'category': self.category.pk,
                'title': 'Lorem ipsum dolor met!',
                'post': 'Check our l33t place!',
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_empty_input(self):
        """validate_post handles empty input"""
        response = self.client.post(
            self.api_link, data={
                'category': self.category.pk,
            }
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            self.api_link, data={
                'category': self.category.pk,
                'title': '',
                'post': '',
            }
        )
        self.assertEqual(response.status_code, 400)
