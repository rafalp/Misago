from datetime import timedelta
from io import StringIO

import pytest
from django.core import management
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ..management.commands import clearattachments
from ..models import Attachment


def call_command():
    command = clearattachments.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_clearattachments_command_does_nothing_if_there_are_no_attachments(db):
    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 0",
    )


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_omits_recent_attachment_not_marked_for_deletion(
    user, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 0",
    )

    attachment.refresh_from_db()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_omits_old_attachment_with_post(
    user, text_file, attachment_factory, post
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    attachment.uploaded_at = timezone.now() - timedelta(hours=3)
    attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 0",
    )

    attachment.refresh_from_db()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_deletes_marked_attachment(
    user, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user, is_deleted=True)

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 1",
        "- Unused: 0",
    )

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_deletes_old_unused_attachment(
    user, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    attachment.uploaded_at = timezone.now() - timedelta(hours=3)
    attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 1",
    )

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()
