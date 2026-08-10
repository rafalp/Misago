from ..postprocess import should_post_process_post_content


def test_should_post_process_post_content_returns_true_if_post_has_code_to_highlight(
    post,
):
    post.metadata["highlight_code"] = True
    assert should_post_process_post_content(post)


def test_should_post_process_post_content_returns_false_if_post_has_no_code_to_highlight(
    post,
):
    post.metadata["highlight_code"] = False
    assert not should_post_process_post_content(post)


def test_should_post_process_post_content_returns_false_if_post_metadata_has_no_highlight_code_entry(
    post,
):
    assert not should_post_process_post_content(post)
