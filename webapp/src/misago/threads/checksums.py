from ..markup import checksums


def is_post_valid(post):
    valid_checksum = make_post_checksum(post)
    return post.checksum == valid_checksum


def make_post_checksum(post):
    post_seeds = [str(v) for v in (post.id, str(post.posted_on.date()))]
    return checksums.make_checksum(post.parsed, post_seeds)


def update_post_checksum(post):
    post.checksum = make_post_checksum(post)
    return post.checksum
