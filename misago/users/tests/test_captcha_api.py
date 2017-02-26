from django.test import TestCase
from django.urls import reverse

from misago.conf import settings


class AuthenticateAPITests(TestCase):
    def setUp(self):
        self.api_link = reverse('misago:api:captcha-question')

    def tearDown(self):
        settings.reset_settings()

    def test_api_no_qa_is_set(self):
        """qa api returns 404 if no QA question is set"""
        settings.override_setting('qa_question', '')

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_api_get_question(self):
        """qa api returns valid QA question"""
        settings.override_setting('qa_question', 'Do you like pies?')
        settings.override_setting('qa_help_text', 'Type in "yes".')

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['question'], 'Do you like pies?')
        self.assertEqual(response_json['help_text'], 'Type in "yes".')
