import os
from io import StringIO

import pytest
from django.core import management
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import CommandError

from ...conf.test import override_dynamic_settings
from ..management.commands import processimageattachments


def call_command(after: int | None = None):
    command = processimageattachments.Command()

    out = StringIO()
    management.call_command(command, after=after, stdout=out, stderr=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_regenerateattachmentthumbnails_command_does_nothing_if_there_are_no_attachments(
    db,
):
    command_output = call_command()
    assert command_output == ("No attachments to process exist",)


def test_regenerateattachmentthumbnails_command_excludes_attachments_without_uploads(
    broken_image_attachment,
):
    command_output = call_command()
    assert command_output == ("No attachments to process exist",)


def test_regenerateattachmentthumbnails_command_skips_file_attachments(text_attachment):
    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{text_attachment.id}: text.txt -> not image",
    )


def test_regenerateattachmentthumbnails_command_skips_video_attachments(
    video_attachment,
):
    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{video_attachment.id}: video.mp4 -> not image",
    )


def test_regenerateattachmentthumbnails_command_handles_attachments_with_upload_not_existing(
    image_attachment,
):
    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png -> file not found",
    )


def test_regenerateattachmentthumbnails_command_handles_attachments_with_broken_images(
    image_attachment, image_invalid, teardown_attachments
):
    with open(image_invalid, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png -> cannot identify image format",
    )


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_sets_image_dimensions(
    image_attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.dimensions = None
        image_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png",
    )

    image_attachment.refresh_from_db()
    assert image_attachment.dimensions == "50x50"


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_updates_image_dimensions(
    image_attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.dimensions = "123x456"
        image_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png",
    )

    image_attachment.refresh_from_db()
    assert image_attachment.dimensions == "50x50"


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_doesnt_generate_small_image_thumbnail(
    image_attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png",
    )

    image_attachment.refresh_from_db()
    assert not image_attachment.thumbnail
    assert not image_attachment.thumbnail_dimensions
    assert not image_attachment.thumbnail_size


@override_dynamic_settings(
    attachment_thumbnail_width=3000, attachment_thumbnail_height=3000
)
def test_regenerateattachmentthumbnails_command_deletes_small_image_thumbnail(
    image_attachment, image_small, teardown_attachments
):
    with open(image_small, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.thumbnail = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.thumbnail_dimensions = "50x50"
        image_attachment.thumbnail_size = 400
        image_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png",
    )

    assert not os.path.exists(image_attachment.thumbnail.path)

    image_attachment.refresh_from_db()
    assert not image_attachment.thumbnail
    assert not image_attachment.thumbnail_dimensions
    assert not image_attachment.thumbnail_size


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_generates_large_image_thumbnail(
    image_attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png",
    )

    image_attachment.refresh_from_db()
    assert image_attachment.thumbnail
    assert image_attachment.thumbnail_dimensions == "50x50"
    assert image_attachment.thumbnail_size

    assert os.path.exists(image_attachment.thumbnail.path)


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_generates_new_large_image_thumbnail(
    image_attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.thumbnail = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.thumbnail_dimensions = "150x150"
        image_attachment.thumbnail_size = 400
        image_attachment.save()

    command_output = call_command()
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png",
    )

    assert not os.path.exists(image_attachment.thumbnail.path)

    image_attachment.refresh_from_db()
    assert image_attachment.thumbnail
    assert image_attachment.thumbnail_dimensions == "50x50"
    assert image_attachment.thumbnail_size

    assert os.path.exists(image_attachment.thumbnail.path)


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
    image_attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.save()

    command_output = call_command(after=image_attachment.id + 1)
    assert command_output == (
        "Attachments to process: 1",
        "",
        "Processing:",
        f"#{image_attachment.id}: image.png",
    )

    image_attachment.refresh_from_db()
    assert image_attachment.thumbnail
    assert image_attachment.thumbnail_dimensions == "50x50"
    assert image_attachment.thumbnail_size

    assert os.path.exists(image_attachment.thumbnail.path)


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_after_option_excludes_attachments_with_equal_id(
    image_attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.save()

    command_output = call_command(after=image_attachment.id)
    assert command_output == ("No attachments to process exist",)


@override_dynamic_settings(
    attachment_thumbnail_width=50, attachment_thumbnail_height=50
)
def test_regenerateattachmentthumbnails_command_after_option_excludes_attachments_with_greater_id(
    image_attachment, image_large, teardown_attachments
):
    with open(image_large, "rb") as fp:
        image_attachment.upload = SimpleUploadedFile(
            "image.png", fp.read(), "image/png"
        )
        image_attachment.save()

    command_output = call_command(after=image_attachment.id)
    assert command_output == ("No attachments to process exist",)
