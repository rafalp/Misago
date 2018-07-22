import os

from django.core.files import File

from misago.users.datadownloads import (
    expire_user_data_download, request_user_data_download, user_has_data_download_request
)
from misago.users.models import DataDownload
from misago.users.testutils import AuthenticatedUserTestCase


TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfiles')
TEST_FILE_PATH = os.path.join(TESTFILES_DIR, 'avatar.png')


class UserHasRequestedDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_returns_false_for_no_download(self):
        """user_has_data_download_request returns false if user has no requests in progress"""
        self.assertFalse(user_has_data_download_request(self.user))

    def test_util_returns_false_for_ready_download(self):
        """user_has_data_download_request returns false if user has ready download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY
        data_download.save()

        self.assertFalse(user_has_data_download_request(self.user))

    def test_util_returns_false_for_expired_download(self):
        """user_has_data_download_request returns false if user has expired download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_EXPIRED
        data_download.save()
        
        self.assertFalse(user_has_data_download_request(self.user))

    def test_util_returns_true_for_pending_download(self):
        """user_has_data_download_request returns true if user has pending download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PENDING
        data_download.save()
        
        self.assertTrue(user_has_data_download_request(self.user))

    def test_util_returns_true_for_processing_download(self):
        """user_has_data_download_request returns true if user has processing download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PROCESSING
        data_download.save()
        
        self.assertTrue(user_has_data_download_request(self.user))


class RequestUserDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_creates_data_download_for_user_with_them_as_requester(self):
        """request_user_data_download created valid data download for user"""
        data_download = request_user_data_download(self.user)

        self.assertEqual(data_download.user, self.user)
        self.assertEqual(data_download.requester, self.user)
        self.assertEqual(data_download.requester_name, self.user.username)
        self.assertEqual(data_download.status, DataDownload.STATUS_PENDING)

    def test_util_creates_data_download_for_user_explicit_requester(self):
        """request_user_data_download created valid data download for user with other requester"""
        requester = self.get_superuser()
        data_download = request_user_data_download(self.user, requester)

        self.assertEqual(data_download.user, self.user)
        self.assertEqual(data_download.requester, requester)
        self.assertEqual(data_download.requester_name, requester.username)
        self.assertEqual(data_download.status, DataDownload.STATUS_PENDING)


class ExpireUserDataDownloadTests(AuthenticatedUserTestCase):
    def test_util_marks_download_as_expired(self):
        """expire_user_data_download changed data download status to expired"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY

        with open(TEST_FILE_PATH, 'rb') as download_file:
            data_download.file = File(download_file)
            data_download.save()

        expire_user_data_download(data_download)

        self.assertEqual(data_download.status, DataDownload.STATUS_EXPIRED)

    def test_util_deletes_file(self):
        """expire_user_data_download deleted file associated with download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY

        with open(TEST_FILE_PATH, 'rb') as download_file:
            data_download.file = File(download_file)
            data_download.save()

        download_file_path = data_download.file.path

        expire_user_data_download(data_download)

        self.assertFalse(data_download.file)
        self.assertFalse(os.path.isdir(download_file_path))

    def test_util_expires_download_without_file(self):
        """expire_user_data_download handles missing download file"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY

        expire_user_data_download(data_download)

        self.assertEqual(data_download.status, DataDownload.STATUS_EXPIRED)
