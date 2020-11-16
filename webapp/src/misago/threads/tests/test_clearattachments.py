from datetime import timedelta
from io import StringIO

import pytest
from django.core import management
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..management.commands import clearattachments
from ..models import Attachment, AttachmentType


@pytest.fixture
def attachment_type(db):
    return AttachmentType.objects.order_by("id").last()


def create_attachment(attachment_type, uploaded_on, post=None):
    return Attachment.objects.create(
        secret=Attachment.generate_new_secret(),
        post=post,
        filetype=attachment_type,
        size=1000,
        uploaded_on=uploaded_on,
        uploader_name="User",
        uploader_slug="user",
        filename="testfile_%s.zip" % (Attachment.objects.count() + 1),
    )


def call_command():
    command = clearattachments.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return out.getvalue().strip().splitlines()[-1].strip()


def test_command_works_if_there_are_no_attachments(db):
    command_output = call_command()
    assert command_output == "No unused attachments were cleared"


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_recent_attachment_is_not_cleared(attachment_type):
    attachment = create_attachment(attachment_type, timezone.now())
    command_output = call_command()
    assert command_output == "No unused attachments were cleared"


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_old_used_attachment_is_not_cleared(attachment_type, post):
    uploaded_on = timezone.now() - timedelta(hours=3)
    attachment = create_attachment(attachment_type, uploaded_on, post)
    command_output = call_command()
    assert command_output == "No unused attachments were cleared"


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_old_unused_attachment_is_cleared(attachment_type):
    uploaded_on = timezone.now() - timedelta(hours=3)
    attachment = create_attachment(attachment_type, uploaded_on)
    command_output = call_command()
    assert command_output == "Cleared 1 attachments"

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()
