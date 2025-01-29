from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse

from ...permissions.checkutils import PermissionCheckResult
from ..html import render_ast_to_html
from ..metadata import create_ast_metadata
from ..richtext import replace_rich_text_tokens


def test_replace_rich_text_tokens_replaces_default_spoiler_summary(
    parser_context, parse_markup, snapshot
):
    ast = parse_markup("[spoiler]Hello world![/spoiler]")
    metadata = create_ast_metadata(parser_context, ast)
    html = render_ast_to_html(parser_context, ast, metadata)
    assert snapshot == replace_rich_text_tokens(html)


def test_replace_rich_text_tokens_replaces_attachment_with_image(attachment):
    attachment.name = "image.png"
    attachment.slug = "image-png"
    attachment.filetype_id = "png"
    attachment.upload = "attachments/image.png"
    attachment.dimensions = "400x150"
    attachment.save()

    html = f"<attachment={attachment.name}:{attachment.slug}:{attachment.id}>"
    data = {"attachment_errors": {}, "attachments": {attachment.id: attachment}}

    result = replace_rich_text_tokens(html, data)
    assert f'href="{attachment.get_details_url()}"' in result
    assert f'href="{attachment.get_absolute_url()}"' in result
    assert f'src="{attachment.get_absolute_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_thumbnail(attachment):
    attachment.name = "image.png"
    attachment.slug = "image-png"
    attachment.filetype_id = "png"
    attachment.upload = "attachments/image.png"
    attachment.dimensions = "400x150"
    attachment.thumbnail = "attachments/thumbnail.png"
    attachment.save()

    html = f"<attachment={attachment.name}:{attachment.slug}:{attachment.id}>"
    data = {"attachment_errors": {}, "attachments": {attachment.id: attachment}}

    result = replace_rich_text_tokens(html, data)
    assert f'href="{attachment.get_details_url()}"' in result
    assert f'href="{attachment.get_absolute_url()}"' in result
    assert f'src="{attachment.get_thumbnail_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_video(attachment):
    attachment.name = "video.mp4"
    attachment.slug = "video-mp4"
    attachment.filetype_id = "mp4"
    attachment.upload = "attachments/video.mp4"
    attachment.dimensions = None
    attachment.save()

    html = f"<attachment={attachment.name}:{attachment.slug}:{attachment.id}>"
    data = {"attachment_errors": {}, "attachments": {attachment.id: attachment}}

    result = replace_rich_text_tokens(html, data)
    assert f'href="{attachment.get_details_url()}"' in result
    assert f'src="{attachment.get_absolute_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_file_link(attachment):
    attachment.name = "document.pdf"
    attachment.slug = "document-pdf"
    attachment.filetype_id = "pdf"
    attachment.upload = "attachments/document.pdf"
    attachment.dimensions = None
    attachment.save()

    html = f"<attachment={attachment.name}:{attachment.slug}:{attachment.id}>"
    data = {"attachment_errors": {}, "attachments": {attachment.id: attachment}}

    result = replace_rich_text_tokens(html, data)
    assert attachment.name in result
    assert f'href="{attachment.get_details_url()}"' in result
    assert f'href="{attachment.get_absolute_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_without_upload_with_broken_link(
    attachment,
):
    attachment.name = "image.png"
    attachment.slug = "image-png"
    attachment.filetype_id = "png"
    attachment.upload = None
    attachment.dimensions = "400x150"
    attachment.save()

    html = f"<attachment={attachment.name}:{attachment.slug}:{attachment.id}>"
    data = {"attachment_errors": {}, "attachments": {attachment.id: attachment}}

    result = replace_rich_text_tokens(html, data)
    assert attachment.name in result
    assert f'href="{attachment.get_details_url()}"' not in result
    assert f'href="{attachment.get_absolute_url()}"' not in result


def test_replace_rich_text_tokens_replaces_permission_denied_attachment_with_error():
    error = PermissionCheckResult(PermissionDenied("Lorem ipsum dolor met"))
    download_url = reverse(
        "misago:attachment-download", kwargs={"slug": "image-png", "id": 123}
    )
    details_url = reverse(
        "misago:attachment-details", kwargs={"slug": "image-png", "id": 123}
    )

    html = "<attachment=image.png:image-png:123>"
    data = {"attachment_errors": {123: error}, "attachments": {}}

    result = replace_rich_text_tokens(html, data)
    assert "image.png" in result
    assert "Lorem ipsum dolor met" in result
    assert f'href="{download_url}"' not in result
    assert f'href="{details_url}"' not in result


def test_replace_rich_text_tokens_replaces_not_found_attachment_with_link():
    error = PermissionCheckResult(Http404())
    download_url = reverse(
        "misago:attachment-download", kwargs={"slug": "image-png", "id": 123}
    )
    details_url = reverse(
        "misago:attachment-details", kwargs={"slug": "image-png", "id": 123}
    )

    html = "<attachment=image.png:image-png:123>"
    data = {"attachment_errors": {123: error}, "attachments": {}}

    result = replace_rich_text_tokens(html, data)
    assert "image.png" in result
    assert f'href="{download_url}"' in result
    assert f'href="{details_url}"' in result


def test_replace_rich_text_tokens_replaces_not_existing_attachment_with_link():
    download_url = reverse(
        "misago:attachment-download", kwargs={"slug": "image-png", "id": 123}
    )
    details_url = reverse(
        "misago:attachment-details", kwargs={"slug": "image-png", "id": 123}
    )

    html = "<attachment=image.png:image-png:123>"
    data = {"attachment_errors": {}, "attachments": {}}

    result = replace_rich_text_tokens(html, data)
    assert "image.png" in result
    assert f'href="{download_url}"' in result
    assert f'href="{details_url}"' in result
