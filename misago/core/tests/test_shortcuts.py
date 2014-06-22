from django.core.urlresolvers import reverse
from django.test import TestCase


class PaginateTests(TestCase):
    serialized_rollback = True
    urls = 'misago.core.testproject.urls'

    def test_valid_page_handling(self):
        """Valid page number causes no errors"""
        response = self.client.get(
            reverse('test_pagination', kwargs={'page': 2}))
        self.assertEqual("5,6,7,8,9", response.content)

    def test_invalid_page_handling(self):
        """Invalid page number results in 404 error"""
        response = self.client.get(
            reverse('test_pagination', kwargs={'page': 42}))
        self.assertEqual(response.status_code, 404)

    def test_implicit_page_handling(self):
        """Implicit page number causes no errors"""
        response = self.client.get(
            reverse('test_pagination'))
        self.assertEqual("0,1,2,3,4", response.content)

    def test_explicit_page_handling(self):
        """Explicit page number results in redirect"""
        response = self.client.get(
            reverse('test_pagination', kwargs={'page': 1}))
        valid_url = "http://testserver/forum/test-pagination/"
        self.assertEqual(response['Location'], valid_url)


class ValidateSlugTests(TestCase):
    serialized_rollback = True
    urls = 'misago.core.testproject.urls'

    def test_valid_slug_handling(self):
        """Valid slug causes no interruption in view processing"""
        test_kwargs = {'model_slug': 'eric-the-fish', 'model_id': 1}
        response = self.client.get(
            reverse('validate_slug_view', kwargs=test_kwargs))
        self.assertIn("Allright", response.content)

    def test_invalid_slug_handling(self):
        """Invalid slug returns in redirect to valid page"""
        test_kwargs = {'model_slug': 'lion-the-eric', 'model_id': 1}
        response = self.client.get(
            reverse('validate_slug_view', kwargs=test_kwargs))

        valid_url = "http://testserver/forum/test-valid-slug/eric-the-fish-1/"
        self.assertEqual(response['Location'], valid_url)
