from typing import Iterable

from ..threads.models import Post
from .tasks import upgrade_post_content
from .upgradepost import post_needs_content_upgrade


def save_edited_post(post: Post):
    post.save()

    post.set_search_vector()
    post.save(update_fields=["search_vector"])

    if post_needs_content_upgrade(post):
        upgrade_post_content.delay(post.id, post.sha256_checksum)
