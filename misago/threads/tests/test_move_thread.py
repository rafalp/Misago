from ..move import move_thread


def test_move_thread_moves_thread_to_new_category(
    thread_relations_factory, thread, sibling_category
):
    thread_relations = thread_relations_factory(thread)

    assert move_thread(thread, sibling_category)
    assert thread.category == sibling_category

    thread.refresh_from_db()
    assert thread.category == sibling_category

    thread_relations.assert_category(sibling_category)


def test_move_thread_doesnt_move_thread_already_in_new_category(
    django_assert_num_queries, thread_relations_factory, thread, default_category
):
    thread_relations = thread_relations_factory(thread)

    with django_assert_num_queries(0):
        assert not move_thread(thread, default_category)
        assert thread.category == default_category

    thread.refresh_from_db()
    assert thread.category == default_category

    thread_relations.assert_category(default_category)


def test_move_thread_doesnt_save_thread_if_commit_is_false(
    django_assert_num_queries,
    thread_relations_factory,
    thread,
    default_category,
    sibling_category,
):
    thread_relations = thread_relations_factory(thread)

    with django_assert_num_queries(8):
        assert move_thread(thread, sibling_category, commit=False)
        assert thread.category == sibling_category

    thread.refresh_from_db()
    assert thread.category == default_category

    thread_relations.assert_category(sibling_category)
