from misago.users.testutils import AuthenticatedUserTestCase


class CommonMiddlewareRedirectTests(AuthenticatedUserTestCase):
    def test_slashless_redirect(self):
        """
        Regression test for https://github.com/rafalp/Misago/issues/450

        there shouldn't be crash when request path lacks trailing slash
        """
        response = self.client.get(self.user.get_absolute_url()[:-1])
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response['location'].endswith(self.user.get_absolute_url()))
