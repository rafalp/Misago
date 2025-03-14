import html
import re

from ..parser.highlighter import highlight_syntax
from ..threads.models import Post
from .hooks import (
    post_needs_content_upgrade_hook,
    upgrade_post_content_hook,
    upgrade_post_code_blocks_hook,
)


def post_needs_content_upgrade(post: Post) -> bool:
    return post_needs_content_upgrade_hook(_post_needs_content_upgrade_action, post)


def _post_needs_content_upgrade_action(post: Post) -> bool:
    if post.metadata.get("highlight_code"):
        return True

    return False


def upgrade_post_content(post: Post):
    upgrade_post_content_hook(_upgrade_post_content_action, post)


def _upgrade_post_content_action(post: Post):
    upgrade_post_code_blocks(post)


CODE_BLOCK_PATTERN = re.compile(
    r"\<misago-code(?P<args>.+?)\>(?P<code>.*?)\<\/misago-code\>", re.DOTALL
)


def upgrade_post_code_blocks(post: Post):
    upgrade_post_code_blocks_hook(_upgrade_post_code_blocks_action, post)


def _upgrade_post_code_blocks_action(post: Post):
    if "highlight_code" not in post.metadata:
        return

    if post.metadata["highlight_code"]:
        html = CODE_BLOCK_PATTERN.sub(upgrade_post_code_blocks_syntax, post.parsed)
    else:
        html = None

    post.metadata.pop("highlight_code")

    if html and post.parsed != html:
        post.parsed = html
        post.save(update_fields=["parsed", "metadata"])
    else:
        post.save(update_fields=["metadata"])


def upgrade_post_code_blocks_syntax(match) -> str:
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
