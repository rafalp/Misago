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


def test_replace_rich_text_tokens_replaces_attachment_with_image(image_attachment):

    html = f"<attachment={image_attachment.name}:{image_attachment.slug}:{image_attachment.id}>"
    data = {
        "attachment_errors": {},
        "attachments": {image_attachment.id: image_attachment},
    }

    result = replace_rich_text_tokens(html, data)
    assert f'href="{image_attachment.get_details_url()}"' in result
    assert f'href="{image_attachment.get_absolute_url()}"' in result
    assert f'src="{image_attachment.get_absolute_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_thumbnail(
    image_thumbnail_attachment,
):
    html = f"<attachment={image_thumbnail_attachment.name}:{image_thumbnail_attachment.slug}:{image_thumbnail_attachment.id}>"
    data = {
        "attachment_errors": {},
        "attachments": {image_thumbnail_attachment.id: image_thumbnail_attachment},
    }

    result = replace_rich_text_tokens(html, data)
    assert f'href="{image_thumbnail_attachment.get_details_url()}"' in result
    assert f'href="{image_thumbnail_attachment.get_absolute_url()}"' in result
    assert f'src="{image_thumbnail_attachment.get_thumbnail_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_video(video_attachment):
    html = f"<attachment={video_attachment.name}:{video_attachment.slug}:{video_attachment.id}>"
    data = {
        "attachment_errors": {},
        "attachments": {video_attachment.id: video_attachment},
    }

    result = replace_rich_text_tokens(html, data)
    assert f'href="{video_attachment.get_details_url()}"' in result
    assert f'src="{video_attachment.get_absolute_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_file_link(text_attachment):
    html = f"<attachment={text_attachment.name}:{text_attachment.slug}:{text_attachment.id}>"
    data = {
        "attachment_errors": {},
        "attachments": {text_attachment.id: text_attachment},
    }

    result = replace_rich_text_tokens(html, data)
    assert text_attachment.name in result
    assert f'href="{text_attachment.get_details_url()}"' in result
    assert f'href="{text_attachment.get_absolute_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_without_upload_with_broken_link(
    broken_image_attachment,
):
    html = f"<attachment={broken_image_attachment.name}:{broken_image_attachment.slug}:{broken_image_attachment.id}>"
    data = {
        "attachment_errors": {},
        "attachments": {broken_image_attachment.id: broken_image_attachment},
    }

    result = replace_rich_text_tokens(html, data)
    assert broken_image_attachment.name in result
    assert f'href="{broken_image_attachment.get_details_url()}"' not in result
    assert f'href="{broken_image_attachment.get_absolute_url()}"' not in result


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
