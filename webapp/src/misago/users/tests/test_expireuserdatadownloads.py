import os
from datetime import timedelta
from io import StringIO

from django.core.files import File
from django.core.management import call_command

from ..datadownloads import request_user_data_download
from ..management.commands import expireuserdatadownloads
from ..models import DataDownload
from ..test import AuthenticatedUserTestCase

TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfiles")
TEST_FILE_PATH = os.path.join(TESTFILES_DIR, "avatar.png")


class ExpireUserDataDownloadsTests(AuthenticatedUserTestCase):
    def test_delete_expired_data_download(self):
        """management command deletes expired data download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY
        with open(TEST_FILE_PATH, "rb") as download_file:
            data_download.file = File(download_file)
            data_download.save()

        out = StringIO()
        call_command(expireuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads expired: 1")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_EXPIRED)
        self.assertFalse(updated_data_download.file)

    def test_skip_not_expired_data_download(self):
        """management command skips data download that expires in future"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY
        data_download.expires_on += timedelta(hours=1)
        with open(TEST_FILE_PATH, "rb") as download_file:
            data_download.file = File(download_file)
            data_download.save()

        out = StringIO()
        call_command(expireuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads expired: 0")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_READY)
        self.assertTrue(updated_data_download.file)

    def test_skip_pending_data_download(self):
        """management command skips pending data downloads"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PENDING
        data_download.save()

        out = StringIO()
        call_command(expireuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads expired: 0")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_PENDING)

    def test_skip_processing_data_download(self):
        """management command skips processing data downloads"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PROCESSING
        data_download.save()

        out = StringIO()
        call_command(expireuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads expired: 0")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_PROCESSING)

    def test_skip_expired_data_download(self):
        """management command skips pending data downloads"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_EXPIRED
        data_download.save()

        out = StringIO()
        call_command(expireuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads expired: 0")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_EXPIRED)

    def test_no_expired_data_download(self):
        """management command doesn't error when no data is expired"""
        out = StringIO()
        call_command(expireuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads expired: 0")
