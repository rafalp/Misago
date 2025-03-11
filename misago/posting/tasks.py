import copy
from logging import getLogger

from celery import shared_task

from ..parser.highlighter import highlight_syntax
from ..threads.models import Post

logger = getLogger("misago.posting")


@shared_task(
    name="posting.update-post-html",
    autoretry_for=(Post.DoesNotExist,),
    default_retry_delay=10,
    time_limit=20,
    serializer="json",
)
def update_post_html(post_id: int, checksum: str):
    post = Post.objects.filter(id=post_id).first()
    if not post or post.sha256_checksum != checksum:
        return

    try:
        _update_post_html(post)
        print("POST UPDATE IS DONE")
    except Exception:
        logger.exception("Unexpected error in 'update_post_html'")


def _update_post_html(post: Post):
    org_html = post.parsed
    org_metadata = copy.deepcopy(post.metadata)

    update_post_code_blocks(post)

    if post.parsed != org_html or post.metadata != org_metadata:
        post.save(update_fields=["parsed", "metadata"])


import re
import html

CODE_BLOCK_TOKEN = re.compile(
    r"\<misago-code(?P<args>.+?)\>(?P<code>.*?)\<\/misago-code\>", re.DOTALL
)


def update_post_code_blocks(post: Post):
    post.parsed = CODE_BLOCK_TOKEN.sub(update_post_code_blocks_syntax, post.parsed)


def update_post_code_blocks_syntax(match) -> str:
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
