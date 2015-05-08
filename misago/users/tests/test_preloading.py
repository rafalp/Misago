from misago.users.testutils import UserTestCase


class PreloadUserTests(UserTestCase):
    def test_anonymous_user(self):
        """anon user is preloaded in json"""
        with self.settings(_MISAGO_JS_DEBUG=True):
            response = self.client.get('/misago-preload-data.js')
            self.assertEqual(response.status_code, 200)
            self.assertIn('isAuthenticated": false', response.content)

    def test_authenticated_user(self):
        """auth user is preloaded in json"""
        self.login_user(self.get_authenticated_user())

        with self.settings(_MISAGO_JS_DEBUG=True):
            response = self.client.get('/misago-preload-data.js')
            self.assertEqual(response.status_code, 200)
            self.assertIn('isAuthenticated": true', response.content)
            self.assertIn(self.user.username, response.content)
