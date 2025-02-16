from datetime import timedelta
from io import StringIO
from pathlib import Path

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
    text_attachment,
):
    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 0",
    )

    text_attachment.refresh_from_db()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_omits_old_attachment_with_post(text_attachment, post):
    text_attachment.associate_with_post(post)
    text_attachment.uploaded_at = timezone.now() - timedelta(hours=3)
    text_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 0",
    )

    text_attachment.refresh_from_db()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_deletes_marked_attachment_with_files(
    image_large, image_small, attachment_factory
):
    attachment = attachment_factory(
        image_large, thumbnail_path=image_small, is_deleted=True
    )

    upload_path = Path(attachment.upload.path)
    assert upload_path.exists()

    thumbnail_path = Path(attachment.thumbnail.path)
    assert thumbnail_path.exists()

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 1",
        "- Unused: 0",
    )

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()

    assert not upload_path.exists()
    assert not thumbnail_path.exists()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_deletes_marked_broken_attachment(
    broken_text_attachment,
):
    broken_text_attachment.is_deleted = True
    broken_text_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 1",
        "- Unused: 0",
    )

    with pytest.raises(Attachment.DoesNotExist):
        broken_text_attachment.refresh_from_db()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_deletes_old_unused_attachment_with_files(
    image_large, image_small, attachment_factory
):
    attachment = attachment_factory(image_large, thumbnail_path=image_small)
    attachment.uploaded_at = timezone.now() - timedelta(hours=3)
    attachment.save()

    upload_path = Path(attachment.upload.path)
    assert upload_path.exists()

    thumbnail_path = Path(attachment.thumbnail.path)
    assert thumbnail_path.exists()

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 1",
    )

    with pytest.raises(Attachment.DoesNotExist):
        attachment.refresh_from_db()

    assert not upload_path.exists()
    assert not thumbnail_path.exists()


@override_dynamic_settings(unused_attachments_lifetime=2)
def test_clearattachments_command_deletes_old_broken_unused_attachment(
    broken_text_attachment,
):
    broken_text_attachment.uploaded_at = timezone.now() - timedelta(hours=3)
    broken_text_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments deleted:",
        "",
        "- Marked: 0",
        "- Unused: 1",
    )

    with pytest.raises(Attachment.DoesNotExist):
        broken_text_attachment.refresh_from_db()
