from django.test import TestCase
from django.urls import reverse

from ...conf.test import override_dynamic_settings

test_qa_question = "Do you like pies?"
test_qa_help_text = 'Type in "yes".'


class AuthenticateApiTests(TestCase):
    def setUp(self):
        self.api_link = reverse("misago:api:captcha-question")

    @override_dynamic_settings(qa_question="")
    def test_api_no_qa_is_set(self):
        """qa api returns 404 if no QA question is set"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    @override_dynamic_settings(
        qa_question=test_qa_question, qa_help_text=test_qa_help_text
    )
    def test_api_get_question(self):
        """qa api returns valid QA question"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["question"], test_qa_question)
        self.assertEqual(response_json["help_text"], test_qa_help_text)
