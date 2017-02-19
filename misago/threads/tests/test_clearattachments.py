from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from misago.categories.models import Category
from misago.conf import settings
from misago.threads import testutils
from misago.threads.management.commands import clearattachments
from misago.threads.models import Attachment, AttachmentType


class ClearAttachmentsTests(TestCase):
    def test_no_attachments_sync(self):
        """command works when there are no attachments"""
        command = clearattachments.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, "No attachments were found")

    def test_attachments_sync(self):
        """command synchronizes attachments"""
        filetype = AttachmentType.objects.order_by('id').last()

        # create 5 expired orphaned attachments
        cutoff = timezone.now() - timedelta(minutes=settings.MISAGO_ATTACHMENT_ORPHANED_EXPIRE)
        cutoff -= timedelta(minutes=5)

        for _ in range(5):
            Attachment.objects.create(
                secret=Attachment.generate_new_secret(),
                filetype=filetype,
                size=1000,
                uploaded_on=cutoff,
                uploader_name='bob',
                uploader_slug='bob',
                uploader_ip='127.0.0.1',
                filename='testfile_{}.zip'.format(Attachment.objects.count() + 1),
            )

        # create 5 expired non-orphaned attachments
        category = Category.objects.get(slug='first-category')
        post = testutils.post_thread(category).first_post

        for _ in range(5):
            Attachment.objects.create(
                secret=Attachment.generate_new_secret(),
                filetype=filetype,
                size=1000,
                uploaded_on=cutoff,
                post=post,
                uploader_name='bob',
                uploader_slug='bob',
                uploader_ip='127.0.0.1',
                filename='testfile_{}.zip'.format(Attachment.objects.count() + 1),
            )

        # create 5 fresh orphaned attachments
        for _ in range(5):
            Attachment.objects.create(
                secret=Attachment.generate_new_secret(),
                filetype=filetype,
                size=1000,
                uploader_name='bob',
                uploader_slug='bob',
                uploader_ip='127.0.0.1',
                filename='testfile_{}.zip'.format(Attachment.objects.count() + 1),
            )

        command = clearattachments.Command()

        out = StringIO()
        call_command(command, stdout=out)

        command_output = out.getvalue().splitlines()[-1].strip()
        self.assertEqual(command_output, "Cleared 5 attachments")

        self.assertEqual(Attachment.objects.count(), 10)
