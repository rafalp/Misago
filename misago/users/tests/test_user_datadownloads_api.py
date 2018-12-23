from ..datadownloads import request_user_data_download
from ..test import AuthenticatedUserTestCase


class UserDataDownloadsApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/data-downloads/" % self.user.pk

    def test_get_other_user_exports_anonymous(self):
        """requests to api fails if user is anonymous"""
        self.logout_user()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have to sign in to perform this action."}
        )

    def test_get_other_user_exports(self):
        """requests to api fails if user tries to access other user"""
        other_user = self.get_superuser()
        link = "/api/users/%s/data-downloads/" % other_user.pk

        response = self.client.get(link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't see other users data downloads."}
        )

    def test_get_empty_list(self):
        """api returns empy list"""
        self.assertFalse(self.user.datadownload_set.exists())

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_populated_list(self):
        """api returns list"""
        for _ in range(6):
            request_user_data_download(self.user)
        self.assertTrue(self.user.datadownload_set.exists())

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)
