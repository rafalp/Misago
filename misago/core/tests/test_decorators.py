from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class RequirePostTests(TestCase):
    def test_require_POST_success(self):
        """require_POST decorator allowed POST request"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.client.login(username=test_user.username, password='Pass.123')

        response = self.client.post(reverse('misago:logout'))

        self.assertEqual(response.status_code, 302)

    def test_require_POST_fail(self):
        """require_POST decorator failed on GET request"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.client.login(username=test_user.username, password='Pass.123')

        response = self.client.get(reverse('misago:logout'))

        self.assertEqual(response.status_code, 405)
        self.assertIn("Wrong way", response.content)
