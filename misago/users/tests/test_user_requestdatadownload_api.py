from ...conf.test import override_dynamic_settings
from ..datadownloads import request_user_data_download
from ..test import AuthenticatedUserTestCase


class UserRequestDataDownload(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/request-data-download/" % self.user.pk

    def test_request_other_user_download_anonymous(self):
        """requests to api fails if user is anonymous"""
        self.logout_user()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    def test_request_other_user_download(self):
        """requests to api fails if user tries to access other user"""
        other_user = self.get_superuser()
        link = "/api/users/%s/request-data-download/" % other_user.pk

        response = self.client.post(link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't request data downloads for other users."},
        )

    @override_dynamic_settings(allow_data_downloads=False)
    def test_request_download_disabled(self):
        """request to api fails if own data downloads are disabled"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't download your data."})

    def test_request_download_in_progress(self):
        """request to api fails if user has already requested data download"""
        request_user_data_download(self.user)

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "You can't have more than one data download request at a single time."
                )
            },
        )

    def test_request_download(self):
        """request to api succeeds"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "ok"})

        self.assertTrue(self.user.datadownload_set.exists())
