from misago.threads.models import Post

from .models import PostSnapshot


def create_post_snapshot(post: Post) -> PostSnapshot:
    return PostSnapshot.objects.create(
        post_id=post.id,
        original=post.original,
        parsed=post.parsed,
        checksum=post.checksum,
        search_document=post.search_document,
        search_vector=post.search_vector,
    )


def restore_post_from_snapshot(post: Post, snapshot: PostSnapshot):
    post.original = snapshot.original
    post.parsed = snapshot.parsed
    post.checksum = snapshot.checksum
    post.search_document = snapshot.search_document
    post.search_vector = snapshot.search_vector

    post.save(
        update_fields=[
            "original",
            "parsed",
            "checksum",
            "search_document",
            "search_vector",
        ]
    )
