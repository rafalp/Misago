from django.test.utils import override_settings

from misago.users.dataexport import start_data_export_for_user
from misago.users.testutils import AuthenticatedUserTestCase


class UserStartDataExportApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(UserStartDataExportApiTests, self).setUp()
        self.link = '/api/users/%s/start-data-export/' % self.user.pk

    def test_start_other_user_export_anonymous(self):
        """requests to api fails if user is anonymous"""
        self.logout_user()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This action is not available to guests.",
        })

    def test_start_other_user_export(self):
        """requests to api fails if user tries to access other user"""
        other_user = self.get_superuser()
        link = '/api/users/%s/start-data-export/' % other_user.pk

        response = self.client.post(link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't request data export for other users.",
        })

    @override_settings(MISAGO_ENABLE_EXPORT_OWN_DATA=False)
    def test_start_export_disabled(self):
        """request to api fails if own data exports are disabled"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't export your own data.",
        })

    def test_start_export_in_progress(self):
        """request to api fails if user already has export in progress"""
        start_data_export_for_user(self.user)

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You already have an data export in progress.",
        })

    def test_start_export(self):
        """request to api fails if user already has export in progress"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'detail': "ok",
        })

        self.assertTrue(self.user.dataexport_set.exists())
