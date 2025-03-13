import copy
from logging import getLogger

from celery import shared_task

from ..threads.models import Post
from .upgrade import upgrade_post_code_blocks

logger = getLogger("misago.posting")


@shared_task(
    name="posting.upgrade-post-content",
    autoretry_for=(Post.DoesNotExist,),
    default_retry_delay=10,
    time_limit=20,
    serializer="json",
)
def upgrade_post_content(post_id: int, checksum: str):
    post = Post.objects.filter(id=post_id).first()
    if not post or post.sha256_checksum != checksum:
        return

    try:
        _upgrade_post_content(post)
    except Exception:
        logger.exception("Unexpected error in 'upgrade_post_content'")


def _upgrade_post_content(post: Post):
    org_html = post.parsed
    org_metadata = copy.deepcopy(post.metadata)

    upgrade_post_code_blocks(post)

    if post.parsed != org_html or post.metadata != org_metadata:
        post.save(update_fields=["parsed", "metadata"])
