from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class RequirePostTests(TestCase):
    def test_require_POST_success(self):
        """require_POST decorator allowed POST request"""
        response = self.client.post(reverse('test-require-post'))
        self.assertContains(response, 'Request method: POST')

    def test_require_POST_fail_GET(self):
        """require_POST decorator failed on GET request"""
        response = self.client.get(reverse('test-require-post'))
        self.assertContains(response, "Wrong way", status_code=405)
