import html
import re

from ..parser.highlighter import highlight_syntax
from ..threads.models import Post
from .hooks import (
    highlight_post_code_blocks_hook,
    post_process_post_content_hook,
    should_post_process_post_content_hook,
)


def should_post_process_post_content(post: Post) -> bool:
    return should_post_process_post_content_hook(
        _should_post_process_post_content_action, post
    )


def _should_post_process_post_content_action(post: Post) -> bool:
    if post.metadata.get("highlight_code"):
        return True

    return False


def post_process_post_content(post: Post):
    post_process_post_content_hook(_post_process_post_content_action, post)


def _post_process_post_content_action(post: Post):
    highlight_post_code_blocks(post)


CODE_BLOCK_PATTERN = re.compile(
    r"\<misago-code(?P<args>.+?)\>(?P<code>.*?)\<\/misago-code\>", re.DOTALL
)


def highlight_post_code_blocks(post: Post):
    highlight_post_code_blocks_hook(_highlight_post_code_blocks_action, post)


def _highlight_post_code_blocks_action(post: Post):
    if "highlight_code" not in post.metadata:
        return

    if post.metadata["highlight_code"]:
        html = CODE_BLOCK_PATTERN.sub(
            highlight_post_code_blocks_syntax, post.content_parsed
        )
    else:
        html = None

    post.metadata.pop("highlight_code")

    if html and post.content_parsed != html:
        post.content_parsed = html
        post.save(update_fields=["content_parsed", "metadata"])
    else:
        post.save(update_fields=["metadata"])


def highlight_post_code_blocks_syntax(match) -> str:
    syntax: str | None = None
    code: str | None = None
    args = match.group("args") or ""

    if code := match.group("code"):
        code = html.unescape(code.rstrip())

    if 'syntax="' in args:
        syntax = args[args.index('syntax="') + 8 :]
        syntax = syntax[: syntax.index('"')].strip()

    if not syntax or not code:
        return match.group(0)

    result = highlight_syntax(syntax, code)
    return f"<misago-code{args}>{result}</misago-code>"
