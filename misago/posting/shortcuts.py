from ..threads.models import Post
from .postprocess import should_post_process_post_content
from .tasks import post_process_post_content


def save_edited_post(post: Post):
    post.save()

    post.set_search_vector()
    post.save(update_fields=["search_vector"])

    if should_post_process_post_content(post):
        post_process_post_content.delay(post.id, post.sha256_checksum)
