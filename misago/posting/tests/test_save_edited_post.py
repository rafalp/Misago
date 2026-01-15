from ..shortcuts import save_edited_post


def test_save_edited_post_saves_post(django_assert_num_queries, post):
    with django_assert_num_queries(2):
        save_edited_post(post)
