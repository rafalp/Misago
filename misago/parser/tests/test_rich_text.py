from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse

from ...attachments.models import Attachment
from ...html.element import html_element
from ...permissions.checkutils import PermissionCheckResult
from ..richtext import replace_rich_text_tokens


def attachment_html_element(attachment: Attachment) -> str:
    return html_element(
        "misago-attachment",
        attrs={
            "name": attachment.name,
            "slug": attachment.slug,
            "id": str(attachment.id),
        },
    )


def test_replace_rich_text_tokens_replaces_spoiler(
    parse_to_html, snapshot
):
    html = parse_to_html("[spoiler]Hello world![/spoiler]")
    assert snapshot == replace_rich_text_tokens(html)


def test_replace_rich_text_tokens_replaces_spoiler_with_custom_info(
    parse_to_html, snapshot
):
    html = parse_to_html("[spoiler=Lorem ipsum]Hello world![/spoiler]")
    assert snapshot == replace_rich_text_tokens(html)


def test_replace_rich_text_tokens_replaces_attachment_with_image(image_attachment):
    html = attachment_html_element(image_attachment)
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
    html = attachment_html_element(image_thumbnail_attachment)
    data = {
        "attachment_errors": {},
        "attachments": {image_thumbnail_attachment.id: image_thumbnail_attachment},
    }

    result = replace_rich_text_tokens(html, data)
    assert f'href="{image_thumbnail_attachment.get_details_url()}"' in result
    assert f'href="{image_thumbnail_attachment.get_absolute_url()}"' in result
    assert f'src="{image_thumbnail_attachment.get_thumbnail_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_video(video_attachment):
    html = attachment_html_element(video_attachment)
    data = {
        "attachment_errors": {},
        "attachments": {video_attachment.id: video_attachment},
    }

    result = replace_rich_text_tokens(html, data)
    assert f'href="{video_attachment.get_details_url()}"' in result
    assert f'src="{video_attachment.get_absolute_url()}#t=0.001"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_file_link(text_attachment):
    html = attachment_html_element(text_attachment)
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
    html = attachment_html_element(broken_image_attachment)
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

    html = html_element(
        "misago-attachment",
        attrs={
            "name": "image.png",
            "slug": "image-png",
            "id": "123",
        },
    )
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

    html = html_element(
        "misago-attachment",
        attrs={
            "name": "image.png",
            "slug": "image-png",
            "id": "123",
        },
    )
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

    html = html_element(
        "misago-attachment",
        attrs={
            "name": "image.png",
            "slug": "image-png",
            "id": "123",
        },
    )
    data = {"attachment_errors": {}, "attachments": {}}

    result = replace_rich_text_tokens(html, data)
    assert "image.png" in result
    assert f'href="{download_url}"' in result
    assert f'href="{details_url}"' in result


def test_replace_rich_text_tokens_replaces_minimal_code_block(parse_to_html, snapshot):
    html = parse_to_html("[code]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html)


def test_replace_rich_text_tokens_replaces_code_block_with_syntax(
    parse_to_html, snapshot
):
    html = parse_to_html("[code=php]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html)


def test_replace_rich_text_tokens_replaces_code_block_with_info(
    parse_to_html, snapshot
):
    html = parse_to_html("[code=Example string]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html)


def test_replace_rich_text_tokens_replaces_code_block_with_info_and_syntax(
    parse_to_html, snapshot
):
    html = parse_to_html("[code=Example string, syntax=php]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html)
