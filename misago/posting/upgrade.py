import re
import html

from ..parser.highlighter import highlight_syntax
from ..threads.models import Post


def post_requires_upgrade(post: Post) -> bool:
    if post.metadata.get("highlight_code"):
        return True

    return False


CODE_BLOCK_TOKEN = re.compile(
    r"\<misago-code(?P<args>.+?)\>(?P<code>.*?)\<\/misago-code\>", re.DOTALL
)


def upgrade_post_code_blocks(post: Post):
    if post.metadata.get("highlight_code"):
        post.parsed = CODE_BLOCK_TOKEN.sub(upgrade_post_code_blocks_syntax, post.parsed)
        post.metadata.pop("highlight_code")


def upgrade_post_code_blocks_syntax(match) -> str:
    syntax: str | None = None
    code: str | None = None
    args = match.group("args") or ""

    if match.group("code"):
        code = html.unescape(match.group("code").strip())

    if 'syntax="' in args:
        syntax = args[args.index('syntax="') + 8 :]
        syntax = syntax[: syntax.index('"')].strip()

    if not syntax or not code:
        return match.group(0)

    result = highlight_syntax(syntax, code)
    return f"<misago-code {args}>{result}</misago-code>"
