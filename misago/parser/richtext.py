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
    html = replace_rich_text_code_blocks_tokens(html)

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
    name, slug, id = matchobj.group(1).split(":")

    id = int(id)
    name = name.strip()
    slug = slug.strip()

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


CODE_BLOCK_TOKEN = re.compile(
    r"\<misago-code(?P<args>.+?)\>(?P<code>.*?)\<\/misago-code\>", re.DOTALL
)


def replace_rich_text_code_blocks_tokens(html: str) -> str:
    return CODE_BLOCK_TOKEN.sub(replace_rich_text_code_block, html)


def replace_rich_text_code_block(match) -> str:
    info: str | None = None
    syntax: str | None = None
    language: str | None = None

    if args := match.group("args"):
        info = _extract_arg(args, "info")
        syntax = _extract_arg(args, "syntax")
        language = _extract_arg(args, "language")

    code = match.group("code") or ""

    return render_to_string(
        "misago/rich_text/code_block.html",
        {
            "info": info,
            "syntax": syntax,
            "language": language,
            "code": code,
        },
    )


def _extract_arg(args: str, arg: str) -> str | None:
    arg_html = f'{arg}="'

    if arg_html not in args:
        return None

    info = args[args.index(arg_html) + len(arg_html) :]
    return info[: info.index('"')].strip() or None
