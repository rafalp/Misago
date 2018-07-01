from django.test.utils import override_settings

from misago.users.datadownloads import prepare_user_data_download
from misago.users.testutils import AuthenticatedUserTestCase


class UserPrepareDataDownload(AuthenticatedUserTestCase):
    def setUp(self):
        super(UserPrepareDataDownload, self).setUp()
        self.link = '/api/users/%s/prepare-data-download/' % self.user.pk

    def test_prepare_other_user_download_anonymous(self):
        """requests to api fails if user is anonymous"""
        self.logout_user()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This action is not available to guests.",
        })

    def test_prepare_other_user_download(self):
        """requests to api fails if user tries to access other user"""
        other_user = self.get_superuser()
        link = '/api/users/%s/prepare-data-download/' % other_user.pk

        response = self.client.post(link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't prepare data downloads for other users.",
        })

    @override_settings(MISAGO_ENABLE_DOWNLOAD_OWN_DATA=False)
    def test_prepare_download_disabled(self):
        """request to api fails if own data downloads are disabled"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't download your data.",
        })

    def test_prepare_download_in_progress(self):
        """request to api fails if user already has created data download"""
        prepare_user_data_download(self.user)

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "Your data download is already in preparation.",
        })

    def test_prepare_download(self):
        """request to api succeeds"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'detail': "ok",
        })

        self.assertTrue(self.user.datadownload_set.exists())
