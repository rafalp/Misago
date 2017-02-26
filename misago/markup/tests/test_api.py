# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse

from misago.users.testutils import AuthenticatedUserTestCase


class ParseMarkupApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(ParseMarkupApiTests, self).setUp()

        self.api_link = reverse('misago:api:parse-markup')

    def test_is_anonymous(self):
        """api requires authentication"""
        self.logout_user()

        response = self.client.post(self.api_link)
        self.assertContains(response, "This action is not available to guests.", status_code=403)

    def test_no_data(self):
        """api handles no data"""
        response = self.client.post(self.api_link)
        self.assertContains(response, "You have to enter a message.", status_code=400)

    def test_empty_post(self):
        """api handles empty post"""
        response = self.client.post(self.api_link, {'post': ''})
        self.assertContains(response, "You have to enter a message.", status_code=400)

    def test_invalid_post(self):
        """api handles invalid post type"""
        response = self.client.post(self.api_link, {'post': 123})
        self.assertContains(
            response,
            "Posted message should be at least 5 characters long (it has 3).",
            status_code=400
        )

    def test_valid_post(self):
        """api returns parsed markup for valid post"""
        response = self.client.post(self.api_link, {'post': 'Lorem ipsum dolor met!'})
        self.assertContains(response, "<p>Lorem ipsum dolor met!</p>")
