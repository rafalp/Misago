from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class RequirePostTests(TestCase):
    urls = 'misago.core.testproject.urls'

    def test_require_POST_success(self):
        """require_POST decorator allowed POST request"""
        response = self.client.post(reverse('test-require-post'))
        self.assertContains(response, 'Request method: POST')

    def test_require_POST_fail_GET(self):
        """require_POST decorator failed on GET request"""
        response = self.client.get(reverse('test-require-post'))
        self.assertContains(response, "Wrong way", status_code=405)
