from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.template import Context
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


def test_replace_rich_text_tokens_replaces_attachment_with_image(image_attachment):
    html = attachment_html_element(image_attachment)
    data = {
        "attachment_errors": {},
        "attachments": {image_attachment.id: image_attachment},
    }

    result = replace_rich_text_tokens(html, Context(), data)
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

    result = replace_rich_text_tokens(html, Context(), data)
    assert f'href="{image_thumbnail_attachment.get_details_url()}"' in result
    assert f'href="{image_thumbnail_attachment.get_absolute_url()}"' in result
    assert f'src="{image_thumbnail_attachment.get_thumbnail_url()}"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_video(video_attachment):
    html = attachment_html_element(video_attachment)
    data = {
        "attachment_errors": {},
        "attachments": {video_attachment.id: video_attachment},
    }

    result = replace_rich_text_tokens(html, Context(), data)
    assert f'href="{video_attachment.get_details_url()}"' in result
    assert f'src="{video_attachment.get_absolute_url()}#t=0.001"' in result


def test_replace_rich_text_tokens_replaces_attachment_with_file_link(text_attachment):
    html = attachment_html_element(text_attachment)
    data = {
        "attachment_errors": {},
        "attachments": {text_attachment.id: text_attachment},
    }

    result = replace_rich_text_tokens(html, Context(), data)
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

    result = replace_rich_text_tokens(html, Context(), data)
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

    result = replace_rich_text_tokens(html, Context(), data)
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

    result = replace_rich_text_tokens(html, Context(), data)
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

    result = replace_rich_text_tokens(html, Context(), data)
    assert "image.png" in result
    assert f'href="{download_url}"' in result
    assert f'href="{details_url}"' in result


def test_replace_rich_text_tokens_replaces_quote(parse_to_html, snapshot):
    html = parse_to_html("[quote]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_quote_with_info(parse_to_html, snapshot):
    html = parse_to_html("[quote=Hello world]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_quote_with_missing_post(
    parse_to_html, snapshot
):
    html = parse_to_html("[quote=Anonymouse, post: 1234]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(
        html,
        Context({"BLANK_AVATAR_URL": "blank-avatar.png"}),
        {"posts": {}},
    )


def test_replace_rich_text_tokens_replaces_quote_with_same_thread_anonymous_user_post(
    parse_to_html, snapshot, default_category, thread, post
):
    default_category.id = 1

    thread.id = 20
    thread.title = "Test Thread"
    thread.slug = "test-thread"

    post.id = 1234
    post.thread_id = thread.id
    post.category_id = default_category.id
    post.posted_at = post.posted_at.replace(
        year=2022,
        month=5,
        day=7,
        hour=21,
        minute=37,
        second=15,
        microsecond=0,
    )

    html = parse_to_html("[quote=Anonymouse, post: 1234]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(
        html,
        Context({"BLANK_AVATAR_URL": "blank-avatar.png", "thread": thread}),
        {
            "categories": {default_category.id: default_category},
            "threads": {thread.id: thread},
            "posts": {post.id: post},
            "users": {},
        },
    )


def test_replace_rich_text_tokens_replaces_quote_with_same_thread_user_post(
    parse_to_html, snapshot, default_category, thread, user_reply, user
):
    user.id = 13

    default_category.id = 1

    thread.id = 20

    user_reply.id = 1234
    user_reply.thread_id = thread.id
    user_reply.category_id = default_category.id
    user_reply.poster_id = user.id
    user_reply.posted_at = user_reply.posted_at.replace(
        year=2022,
        month=5,
        day=7,
        hour=21,
        minute=37,
        second=15,
        microsecond=0,
    )

    html = parse_to_html("[quote=Anonymouse, post: 1234]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(
        html,
        Context({"BLANK_AVATAR_URL": "blank-avatar.png", "thread": thread}),
        {
            "categories": {default_category.id: default_category},
            "threads": {thread.id: thread},
            "posts": {user_reply.id: user_reply},
            "users": {user.id: user},
        },
    )


def test_replace_rich_text_tokens_replaces_quote_with_same_thread_invisible_user_post(
    parse_to_html, snapshot, default_category, thread, user_reply, user
):
    user.id = 13

    default_category.id = 1

    thread.id = 20

    user_reply.id = 1234
    user_reply.thread_id = thread.id
    user_reply.category_id = default_category.id
    user_reply.poster_id = user.id
    user_reply.posted_at = user_reply.posted_at.replace(
        year=2022,
        month=5,
        day=7,
        hour=21,
        minute=37,
        second=15,
        microsecond=0,
    )

    html = parse_to_html("[quote=Anonymouse, post: 1234]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(
        html,
        Context({"BLANK_AVATAR_URL": "blank-avatar.png", "thread": thread}),
        {
            "categories": {default_category.id: default_category},
            "threads": {thread.id: thread},
            "posts": {},
            "users": {user.id: user},
        },
    )


def test_replace_rich_text_tokens_replaces_quote_with_other_thread_anonymous_user_post(
    parse_to_html, snapshot, default_category, thread, user_reply, user, other_thread
):
    user.id = 13

    default_category.id = 1

    thread.id = 20

    user_reply.id = 1234
    user_reply.thread_id = thread.id
    user_reply.category_id = default_category.id
    user_reply.poster_id = user.id
    user_reply.posted_at = user_reply.posted_at.replace(
        year=2022,
        month=5,
        day=7,
        hour=21,
        minute=37,
        second=15,
        microsecond=0,
    )

    html = parse_to_html("[quote=Anonymouse, post: 1234]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(
        html,
        Context({"BLANK_AVATAR_URL": "blank-avatar.png", "thread": other_thread}),
        {
            "categories": {default_category.id: default_category},
            "threads": {thread.id: thread},
            "posts": {user_reply.id: user_reply},
            "users": {user.id: user},
        },
    )


def test_replace_rich_text_tokens_replaces_quote_with_other_thread_user_post(
    parse_to_html, snapshot, default_category, thread, post, other_thread
):
    default_category.id = 1

    thread.id = 20
    thread.title = "Test Thread"
    thread.slug = "test-thread"

    post.id = 1234
    post.thread_id = thread.id
    post.category_id = default_category.id
    post.posted_at = post.posted_at.replace(
        year=2022,
        month=5,
        day=7,
        hour=21,
        minute=37,
        second=15,
        microsecond=0,
    )

    html = parse_to_html("[quote=Anonymouse, post: 1234]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(
        html,
        Context({"BLANK_AVATAR_URL": "blank-avatar.png", "thread": other_thread}),
        {
            "categories": {default_category.id: default_category},
            "threads": {thread.id: thread},
            "posts": {post.id: post},
            "users": {},
        },
    )


def test_replace_rich_text_tokens_replaces_quote_with_other_thread_invisible_user_post(
    parse_to_html, snapshot, default_category, thread, post, other_thread
):
    default_category.id = 1

    thread.id = 20

    post.id = 1234
    post.thread_id = thread.id
    post.category_id = default_category.id
    post.posted_at = post.posted_at.replace(
        year=2022,
        month=5,
        day=7,
        hour=21,
        minute=37,
        second=15,
        microsecond=0,
    )

    html = parse_to_html("[quote=Anonymouse, post: 1234]Hello world![/quote]")
    assert snapshot == replace_rich_text_tokens(
        html,
        Context({"BLANK_AVATAR_URL": "blank-avatar.png", "thread": other_thread}),
        {
            "categories": {default_category.id: default_category},
            "threads": {thread.id: thread},
            "posts": {},
            "users": {},
        },
    )


def test_replace_rich_text_tokens_replaces_spoiler(parse_to_html, snapshot):
    html = parse_to_html("[spoiler]Hello world![/spoiler]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_spoiler_with_custom_info(
    parse_to_html, snapshot
):
    html = parse_to_html("[spoiler=Lorem ipsum]Hello world![/spoiler]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_minimal_code_block(parse_to_html, snapshot):
    html = parse_to_html("[code]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_code_block_with_syntax(
    parse_to_html, snapshot
):
    html = parse_to_html("[code=php]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_code_block_with_info(
    parse_to_html, snapshot
):
    html = parse_to_html("[code=Example string]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_code_block_with_info_and_syntax(
    parse_to_html, snapshot
):
    html = parse_to_html("[code=Example string, syntax=php]Hello world![/code]")
    assert snapshot == replace_rich_text_tokens(html, Context())


def test_replace_rich_text_tokens_replaces_youtube_video(parse_to_html, snapshot):
    html = parse_to_html("https://www.youtube.com/watch?v=QzfXag4r7Vo")
    assert snapshot == replace_rich_text_tokens(html, Context())
