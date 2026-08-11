from logging import getLogger

from celery import shared_task

from ..threads.models import Post
from . import processcontent

logger = getLogger("misago.posting")


@shared_task(
    name="posting.process-post-content",
    autoretry_for=(Post.DoesNotExist,),
    default_retry_delay=10,
    time_limit=20,
    serializer="json",
)
def process_post_content(post_id: int, checksum: str):
    post = Post.objects.get(id=post_id)
    if post.sha256_checksum != checksum:
        return

    try:
        processcontent.process_post_content(post)
    except Exception:
        logger.exception("Unexpected error in 'process_post_content'")
