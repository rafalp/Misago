from ..upgradepost import post_needs_content_upgrade


def test_post_needs_content_upgrade_returns_true_if_post_has_code_to_highlight(post):
    post.metadata["highlight_code"] = True
    assert post_needs_content_upgrade(post)


def test_post_needs_content_upgrade_returns_false_if_post_has_no_code_to_highlight(
    post,
):
    post.metadata["highlight_code"] = False
    assert not post_needs_content_upgrade(post)


def test_post_needs_content_upgrade_returns_false_if_post_metadata_has_no_highlight_code_entry(
    post,
):
    assert not post_needs_content_upgrade(post)
