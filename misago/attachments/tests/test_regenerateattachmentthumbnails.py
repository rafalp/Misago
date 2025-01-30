import os
from io import StringIO

import pytest
from django.core import management
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import CommandError

from ...conf.test import override_dynamic_settings
from ..management.commands import regenerateattachmentthumbnails


def call_command(after: int | None = None):
    command = regenerateattachmentthumbnails.Command()

    out = StringIO()
    management.call_command(command, after=after, stdout=out, stderr=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_regenerateattachmentthumbnails_command_does_nothing_if_there_are_no_attachments(
    db,
):
    command_output = call_command()
    assert command_output == ("No attachments to process exist",)


def test_regenerateattachmentthumbnails_command_excludes_attachments_without_uploads(
    attachment,
):
    command_output = call_command()
    assert command_output == ("No attachments to process exist",)


def test_regenerateattachmentthumbnails_command_skips_video_attachments(attachment):
    attachment.name = "video.mp4"
    attachment.filetype_id = "mp4"
    attachment.upload = "attachments/video.mp4"
    attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: video.mp4 -> not image",
    )


def test_regenerateattachmentthumbnails_command_skips_file_attachments(attachment):
    attachment.name = "doc.pdf"
    attachment.filetype_id = "pdf"
    attachment.upload = "attachments/doc.pdf"
    attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: doc.pdf -> not image",
    )


def test_regenerateattachmentthumbnails_command_handles_attachments_with_upload_not_existing(
    attachment,
):
    attachment.upload = "attachments/missing.png"
    attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png -> file not found",
    )


def test_regenerateattachmentthumbnails_command_handles_attachments_with_broken_images(
    attachment, image_invalid, teardown_attachments
):
    with open(image_invalid, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png -> cannot identify image format",
    )


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_sets_image_dimensions(
    attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.dimensions = None
        attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png",
    )

    attachment.refresh_from_db()
    assert attachment.dimensions == "50x50"


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_updates_image_dimensions(
    attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.dimensions = "123x456"
        attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png",
    )

    attachment.refresh_from_db()
    assert attachment.dimensions == "50x50"


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_doesnt_generate_small_image_thumbnail(
    attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png",
    )

    attachment.refresh_from_db()
    assert not attachment.thumbnail
    assert not attachment.thumbnail_dimensions
    assert not attachment.thumbnail_size


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_deletes_small_image_thumbnail(
    attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.thumbnail = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.thumbnail_dimensions = "50x50"
        attachment.thumbnail_size = 400
        attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png",
    )

    assert not os.path.exists(attachment.thumbnail.path)

    attachment.refresh_from_db()
    assert not attachment.thumbnail
    assert not attachment.thumbnail_dimensions
    assert not attachment.thumbnail_size


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_generates_large_image_thumbnail(
    attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png",
    )

    attachment.refresh_from_db()
    assert attachment.thumbnail
    assert attachment.thumbnail_dimensions == "50x50"
    assert attachment.thumbnail_size

    assert os.path.exists(attachment.thumbnail.path)


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_generates_new_large_image_thumbnail(
    attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.thumbnail = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.thumbnail_dimensions = "150x150"
        attachment.thumbnail_size = 400
        attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png",
    )

    assert not os.path.exists(attachment.thumbnail.path)

    attachment.refresh_from_db()
    assert attachment.thumbnail
    assert attachment.thumbnail_dimensions == "50x50"
    assert attachment.thumbnail_size

    assert os.path.exists(attachment.thumbnail.path)


def test_regenerateattachmentthumbnails_command_prints_error_if_after_is_one(db):
    with pytest.raises(CommandError) as exc_info:
        call_command(after=1)

    assert str(exc_info.value) == "'after' arg must be greater than 1"


def test_regenerateattachmentthumbnails_command_prints_error_if_after_is_zero(db):
    with pytest.raises(CommandError) as exc_info:
        call_command(after=0)

    assert str(exc_info.value) == "'after' arg must be greater than 1"


def test_regenerateattachmentthumbnails_command_prints_error_if_after_is_negative(db):
    with pytest.raises(CommandError) as exc_info:
        call_command(after=-5)

    assert str(exc_info.value) == "'after' arg must be greater than 1"


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_after_option_includes_attachments_with_lesser_id(
    attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.save()

    command_output = call_command(after=attachment.id + 1)
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{attachment.id}: image.png",
    )

    attachment.refresh_from_db()
    assert attachment.thumbnail
    assert attachment.thumbnail_dimensions == "50x50"
    assert attachment.thumbnail_size

    assert os.path.exists(attachment.thumbnail.path)


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_after_option_excludes_attachments_with_equal_id(
    attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.save()

    command_output = call_command(after=attachment.id)
    assert command_output == ("No attachments to process exist",)


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_after_option_excludes_attachments_with_greater_id(
    attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        attachment.upload = SimpleUploadedFile("image.png", fp.read(), "image/png")
        attachment.save()

    command_output = call_command(after=attachment.id)
    assert command_output == ("No attachments to process exist",)
