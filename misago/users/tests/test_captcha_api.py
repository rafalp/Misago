import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.conf import settings

class AuthenticateAPITests(TestCase):
    def setUp(self):
        self.api_link = reverse('misago:api:captcha_question',
                                kwargs={'question_id': 1})

    def tearDown(self):
        settings.reset_settings()

    def test_api_no_qa_is_set(self):
        """qa api returns 404 if no QA question is set"""
        settings.override_setting('qa_question', '')

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_api_invalid_qa_id(self):
        """qa api returns QA question only for ID #1"""
        settings.override_setting('qa_question', 'Do you like pies?')

        response = self.client.get(self.api_link.replace('1', '24'))
        self.assertEqual(response.status_code, 404)

    def test_api_get_question_id(self):
        """qa api returns valid QA question for ID #1"""
        settings.override_setting('qa_question', 'Do you like pies?')
        settings.override_setting('qa_help_text', 'Type in "yes".')

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], 1)
        self.assertEqual(response_json['question'], 'Do you like pies?')
        self.assertEqual(response_json['help_text'], 'Type in "yes".')
