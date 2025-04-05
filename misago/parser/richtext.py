from functools import partial

from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string

from ..attachments.models import Attachment
from ..html.replace import (
    replace_html_element,
    replace_html_element_func,
    replace_html_void_element,
    replace_html_void_element_func,
)
from ..permissions.checkutils import PermissionCheckResult
from ..threads.models import Thread
from ..users.models import User
from .hooks import replace_rich_text_tokens_hook


def replace_rich_text_tokens(
    html: str,
    data: dict | None = None,
    user: AnonymousUser | User | None = None,
    thread: Thread | None = None,
) -> str:
    if data is None:
        data = {}

    return replace_rich_text_tokens_hook(
        _replace_rich_text_tokens_action, html, data, user, thread
    )


def _replace_rich_text_tokens_action(
    html: str,
    data: dict,
    user: AnonymousUser | User | None = None,
    thread: Thread | None = None,
) -> str:
    replace_rich_text_attachment_partial = replace_html_void_element_func(
        partial(
            replace_rich_text_attachment,
            data.get("attachments") or {},
            data.get("attachment_errors") or {},
        )
    )

    replace_rich_text_quote_block_partial = replace_html_element_func(
        partial(replace_rich_text_quote_block, data, thread)
    )

    html = replace_html_void_element(
        html, "misago-attachment", replace_rich_text_attachment_partial
    )
    html = replace_html_element(
        html, "misago-quote", replace_rich_text_quote_block_partial
    )
    html = replace_html_element(html, "misago-code", replace_rich_text_code_block)
    html = replace_html_element(html, "misago-spoiler", replace_rich_text_spoiler_block)

    return html


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


def replace_rich_text_quote_block(
    data: dict,
    thread: Thread | None,
    html: str,
    content: str,
    args: dict | None,
) -> str:
    post_id = None
    post = None
    poster = None
    post_thread = None

    try:
        if args:
            post_id = int(args.get("post"))
    except (TypeError, ValueError):
        pass

    if post_id:
        post = data["posts"].get(post_id)

    if post:
        if post.poster_id:
            poster = data["users"].get(post.poster_id)
        if thread and post.thread_id != thread.id:
            post_thread = data["threads"].get(post.thread_id)

    # DELETE ME LATER
    if post_id and not post:
        from misago.threads.models import Post

        post = Post.objects.select_related("poster", "thread", "thread__category").get(
            id=post_id
        )
        poster = post.poster
        post_thread = post.thread

    return render_to_string(
        "misago/rich_text/quote_block.html",
        {
            "thread": post_thread,
            "post": post,
            "poster": poster,
            "poster_name": args.get("user") if args else None,
            "info": args.get("info") if args else None,
            "content": content,
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
