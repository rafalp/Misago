from ..threads.models import Post
from .processcontent import should_process_post_content
from .tasks import process_post_content


def save_edited_post(post: Post):
    post.save()

    if should_process_post_content(post):
        process_post_content.delay(post.id, post.sha256_checksum)
