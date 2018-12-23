from django.urls import reverse

from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase


class ValidatePostTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.api_link = reverse("misago:api:thread-list")

    def test_title_validation(self):
        """validate_post tests title"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Check our l33t CaSiNo!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"non_field_errors": ["Don't discuss gambling!"]}
        )

        # clean title passes validation
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Check our l33t place!",
                "post": "Lorem ipsum dolor met!",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_post_validation(self):
        """validate_post tests post content"""
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Lorem ipsum dolor met!",
                "post": "Check our l33t CaSiNo!",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"non_field_errors": ["Don't discuss gambling!"]}
        )

        # clean post passes validation
        response = self.client.post(
            self.api_link,
            data={
                "category": self.category.pk,
                "title": "Lorem ipsum dolor met!",
                "post": "Check our l33t place!",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_empty_input(self):
        """validate_post handles empty input"""
        response = self.client.post(self.api_link, data={"category": self.category.pk})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": ["You have to enter thread title."],
                "post": ["You have to enter a message."],
            },
        )

        response = self.client.post(
            self.api_link, data={"category": self.category.pk, "title": "", "post": ""}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": ["This field may not be blank."],
                "post": ["This field may not be blank."],
            },
        )
