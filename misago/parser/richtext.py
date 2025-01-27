import re
from functools import partial

from django.template.loader import render_to_string
from django.utils.translation import pgettext

from ..attachments.models import Attachment
from ..permissions.checkutils import PermissionCheckResult
from .hooks import replace_rich_text_tokens_hook


def replace_rich_text_tokens(html: str, data: dict | None = None) -> str:
    if data is None:
        data = {}

    return replace_rich_text_tokens_hook(_replace_rich_text_tokens_action, html, data)


def _replace_rich_text_tokens_action(html: str, data) -> str:
    html = replace_rich_text_tokens_attachments(
        html, data.get("attachments"), data.get("attachment_errors")
    )

    return html


ATTACHMENT_TOKEN = re.compile(r"\<attachment=(.+?)\>")


def replace_rich_text_tokens_attachments(
    html: str,
    attachments: dict[int, Attachment] | None,
    attachment_errors: dict[int, PermissionCheckResult],
) -> str:
    attachments = attachments or {}
    attachment_errors = attachment_errors or {}

    replace = partial(
        replace_rich_text_attachment_token, attachments, attachment_errors
    )

    return ATTACHMENT_TOKEN.sub(replace, html)


def replace_rich_text_attachment_token(
    attachments: dict[int, Attachment],
    attachment_errors: dict[int, PermissionCheckResult],
    matchobj: re.Match,
) -> str:
    name, id = matchobj.group(1).split(":")

    id = int(id)
    name = name.strip()

    attachment = attachments.get(id)
    error = attachment_errors.get(id)

    if attachment and not error:
        attachment = attachments[id]
        if attachment.filetype.is_image:
            template_name = "misago/rich_text/attachment_image.html"
        elif attachment.filetype.is_video:
            template_name = "misago/rich_text/attachment_video.html"
        else:
            template_name = "misago/rich_text/attachment_file.html"

        return render_to_string(template_name, {"attachment": attachment})

    if error and error.permission_denied:
        return render_to_string(
            "misago/rich_text/attachment_permission_denied.html",
            {
                "attachment": attachment,
                "error": error.error,
                "name": name,
            },
        )

    return render_to_string(
        "misago/rich_text/attachment_not_found.html",
        {
            "attachment": attachment,
            "name": name,
        },
    )
