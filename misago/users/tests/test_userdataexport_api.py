from misago.users.testutils import AuthenticatedUserTestCase


class UserDataExportApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(UserDataExportApiTests, self).setUp()
        self.link = '/api/users/%s/start-data-export/' % self.user.pk

    def test_other_user_export(self):
        """requests to api error if user tries to access other user"""
        other_user = self.get_superuser()
        link = '/api/users/%s/start-data-export/' % other_user.pk

        response = self.client.post(link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can\'t request data export for other users.",
        })
