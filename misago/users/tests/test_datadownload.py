from misago.users.datadownload import is_user_preparing_data_download, prepare_user_data_download
from misago.users.models import DataDownload
from misago.users.testutils import AuthenticatedUserTestCase


class IsUserPreparingDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_returns_false_for_no_download(self):
        """is_user_preparing_data_download returns false if user has no preparation in progress"""
        self.assertFalse(is_user_preparing_data_download(self.user))

    def test_util_returns_false_for_ready_download(self):
        """is_user_preparing_data_download returns false if user has ready download"""
        data_download = prepare_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY
        data_download.save()

        self.assertFalse(is_user_preparing_data_download(self.user))

    def test_util_returns_false_for_expired_download(self):
        """is_user_preparing_data_download returns false if user has expired download"""
        data_download = prepare_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_EXPIRED
        data_download.save()
        
        self.assertFalse(is_user_preparing_data_download(self.user))

    def test_util_returns_true_for_pending_download(self):
        """is_user_preparing_data_download returns true if user has pending download"""
        data_download = prepare_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PENDING
        data_download.save()
        
        self.assertTrue(is_user_preparing_data_download(self.user))

    def test_util_returns_true_for_processing_download(self):
        """is_user_preparing_data_download returns true if user has processing download"""
        data_download = prepare_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PROCESSING
        data_download.save()
        
        self.assertTrue(is_user_preparing_data_download(self.user))


class PrepareUserDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_creates_data_download_for_user_with_them_as_requester(self):
        """prepare_user_data_download prepared valid data download for user"""
        data_download = prepare_user_data_download(self.user)

        self.assertEqual(data_download.user, self.user)
        self.assertEqual(data_download.requester, self.user)
        self.assertEqual(data_download.requester_name, self.user.username)
        self.assertEqual(data_download.status, DataDownload.STATUS_PENDING)

    def test_util_creates_data_download_for_user_explicit_requester(self):
        """prepare_user_data_download prepared valid data download for user with other requester"""
        requester = self.get_superuser()
        data_download = prepare_user_data_download(self.user, requester)

        self.assertEqual(data_download.user, self.user)
        self.assertEqual(data_download.requester, requester)
        self.assertEqual(data_download.requester_name, requester.username)
        self.assertEqual(data_download.status, DataDownload.STATUS_PENDING)
