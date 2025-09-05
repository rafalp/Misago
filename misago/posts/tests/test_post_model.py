def test_post_sha256_checksum(post):
    assert post.sha256_checksum


def test_post_set_search_document(thread, post):
    post.set_search_document(thread, "Lorem ipsum")
    assert post.search_document == f"{thread.title}\n\nLorem ipsum"


def test_post_set_search_vector(thread, post):
    post.set_search_document(thread, "Lorem ipsum")
    post.set_search_vector()
    assert post.search_vector
