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
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {
                'detail': "This action is not available to guests.",
            },
        )

    def test_no_data(self):
        """api handles no data"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'markup': ["This field is required."],
            },
        )

    def test_invalid_data(self):
        """api handles post that is invalid type"""
        response = self.client.post(self.api_link, '[]', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'non_field_errors': ["Invalid data. Expected a dictionary, but got list."],
            },
        )

        response = self.client.post(self.api_link, '123', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'non_field_errors': ["Invalid data. Expected a dictionary, but got int."],
            },
        )

        response = self.client.post(self.api_link, '"string"', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'non_field_errors': ["Invalid data. Expected a dictionary, but got str."],
            },
        )

        response = self.client.post(self.api_link, 'malformed', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'detail': 'JSON parse error - Expecting value: line 1 column 1 (char 0)',
            },
        )

    def test_empty_markup(self):
        """api handles empty markup"""
        response = self.client.post(self.api_link, {'markup': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'markup': ["You have to enter a message."],
            },
        )

        # regression test for #929
        response = self.client.post(self.api_link, {'markup': '\n'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'markup': ["You have to enter a message."],
            },
        )

    def test_invalid_markup(self):
        """api handles invalid markup type"""
        response = self.client.post(self.api_link, {'markup': 123})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'markup': [
                    "Posted message should be at least 5 characters long (it has 3)."
                ],
            },
        )
        
    def test_valid_markup(self):
        """api returns parsed markup for valid markup"""
        response = self.client.post(self.api_link, {'markup': 'Lorem ipsum dolor met!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'parsed': '<p>Lorem ipsum dolor met!</p>',
            },
        )
