from logging import getLogger

from celery import shared_task

from ..threads.models import Post
from . import upgradepost

logger = getLogger("misago.posting")


@shared_task(
    name="posting.upgrade-post-content",
    autoretry_for=(Post.DoesNotExist,),
    default_retry_delay=10,
    time_limit=20,
    serializer="json",
)
def upgrade_post_content(post_id: int, checksum: str):
    post = Post.objects.get(id=post_id)
    if post.sha256_checksum != checksum:
        return

    try:
        upgradepost.upgrade_post_content(post)
    except Exception:
        logger.exception("Unexpected error in 'upgrade_post_content'")
