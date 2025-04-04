from functools import partial

from django.template.loader import render_to_string

from ..attachments.models import Attachment
from ..html.replace import (
    replace_html_element,
    replace_html_element_func,
    replace_html_void_element,
    replace_html_void_element_func,
)
from ..permissions.checkutils import PermissionCheckResult
from .hooks import replace_rich_text_tokens_hook


def replace_rich_text_tokens(html: str, data: dict | None = None) -> str:
    if data is None:
        data = {}

    return replace_rich_text_tokens_hook(_replace_rich_text_tokens_action, html, data)


def _replace_rich_text_tokens_action(html: str, data) -> str:
    html = replace_rich_text_attachments(
        html, data.get("attachments"), data.get("attachment_errors")
    )
    html = replace_html_element(html, "misago-code", replace_rich_text_code_block)
    html = replace_html_element(html, "misago-spoiler", replace_rich_text_spoiler_block)

    return html


def replace_rich_text_attachments(
    html: str,
    attachments: dict[int, Attachment] | None,
    attachment_errors: dict[int, PermissionCheckResult],
) -> str:
    attachments = attachments or {}
    attachment_errors = attachment_errors or {}

    replace = replace_html_void_element_func(
        partial(replace_rich_text_attachment, attachments, attachment_errors)
    )

    return replace_html_void_element(html, "misago-attachment", replace)


def replace_rich_text_attachment(
    attachments: dict[int, Attachment],
    attachment_errors: dict[int, PermissionCheckResult],
    html: str,
    args: dict,
) -> str:
    id = int(args["id"])
    name = args["name"]
    slug = args["slug"]

    error = attachment_errors.get(id)
    if error is not None and error.permission_denied:
        return render_to_string(
            "misago/rich_text/attachment_permission_denied.html",
            {
                "error": error.error,
                "name": name,
            },
        )

    if attachment := attachments.get(id):
        if not attachment.upload:
            template_name = "misago/rich_text/attachment_broken.html"
        elif attachment.filetype.is_image:
            template_name = "misago/rich_text/attachment_image.html"
        elif attachment.filetype.is_video:
            template_name = "misago/rich_text/attachment_video.html"
        else:
            template_name = "misago/rich_text/attachment_file.html"

        return render_to_string(template_name, {"attachment": attachment})

    return render_to_string(
        "misago/rich_text/attachment_link.html",
        {
            "name": name,
            "slug": slug,
            "id": id,
        },
    )


@replace_html_element_func
def replace_rich_text_code_block(html: str, code: str, args: dict | None) -> str:
    return render_to_string(
        "misago/rich_text/code_block.html",
        {
            "info": args.get("info") if args else None,
            "syntax": args.get("syntax") if args else None,
            "language": args.get("language") if args else None,
            "code": code,
        },
    )


@replace_html_element_func
def replace_rich_text_spoiler_block(html: str, content: str, args: dict | None) -> str:
    return render_to_string(
        "misago/rich_text/spoiler_block.html",
        {
            "info": args.get("info") if args else None,
            "content": content,
        },
    )
