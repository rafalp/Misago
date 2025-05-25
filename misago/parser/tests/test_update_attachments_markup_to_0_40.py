from ...attachments.models import Attachment
from ..updates.attachments_0_40 import update_attachments_markup_to_0_40


def test_update_replaces_short_image_markdown_with_attachment_url(db, image_attachment):
    markup = f"!(/a/ds78a6d8sa6d78s6a87d6sa786876dsadsa876d8sa/{image_attachment.id}/?shva=1)"
    new_markup = update_attachments_markup_to_0_40(Attachment, markup)
    assert new_markup == f"<attachment={image_attachment.name}:{image_attachment.id}>"


def test_update_replaces_thumb_short_image_markdown_with_attachment_url(
    db, image_attachment
):
    markup = f"!(/a/thumb/ds78a6d8sa6d78s6a87d6sa786876dsadsa876d8sa/{image_attachment.id}/?shva=1)"
    new_markup = update_attachments_markup_to_0_40(Attachment, markup)
    assert new_markup == f"<attachment={image_attachment.name}:{image_attachment.id}>"
