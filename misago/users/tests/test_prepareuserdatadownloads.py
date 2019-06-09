from io import StringIO

from django.core import mail
from django.core.management import call_command

from ...conf.test import override_dynamic_settings
from ..datadownloads import request_user_data_download
from ..management.commands import prepareuserdatadownloads
from ..models import DataDownload
from ..test import AuthenticatedUserTestCase


class PrepareUserDataDownloadsTests(AuthenticatedUserTestCase):
    @override_dynamic_settings(forum_address="http://test.com/")
    def test_process_pending_data_download(self):
        """management command processes pending data download"""
        data_download = request_user_data_download(self.user)
        self.assertEqual(data_download.status, DataDownload.STATUS_PENDING)

        out = StringIO()
        call_command(prepareuserdatadownloads.Command(), stdout=out)

        command_output = out.getvalue().splitlines()[0].strip()
        self.assertEqual(command_output, "Data downloads prepared: 1")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_READY)
        self.assertTrue(updated_data_download.expires_on > data_download.expires_on)
        self.assertTrue(updated_data_download.file)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "TestUser, your data download is ready"
        )

        absolute_url = "".join(["http://test.com", updated_data_download.file.url])
        self.assertIn(absolute_url, mail.outbox[0].body)

    def test_skip_ready_data_download(self):
        """management command skips ready data download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_READY
        data_download.save()

        out = StringIO()
        call_command(prepareuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads prepared: 0")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_READY)

        self.assertEqual(len(mail.outbox), 0)

    def test_skip_processing_data_download(self):
        """management command skips processing data download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_PROCESSING
        data_download.save()

        out = StringIO()
        call_command(prepareuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads prepared: 0")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_PROCESSING)

        self.assertEqual(len(mail.outbox), 0)

    def test_skip_expired_data_download(self):
        """management command skips expired data download"""
        data_download = request_user_data_download(self.user)
        data_download.status = DataDownload.STATUS_EXPIRED
        data_download.save()

        out = StringIO()
        call_command(prepareuserdatadownloads.Command(), stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Data downloads prepared: 0")

        updated_data_download = DataDownload.objects.get(pk=data_download.pk)
        self.assertEqual(updated_data_download.status, DataDownload.STATUS_EXPIRED)

        self.assertEqual(len(mail.outbox), 0)
