from ..move import move_threads


def test_move_threads_moves_threads_to_new_category(
    thread_relations_factory, thread, user_thread, sibling_category
):
    thread_relations = thread_relations_factory(thread)
    user_thread_relations = thread_relations_factory(user_thread)

    move_threads([thread, user_thread], sibling_category)

    thread.refresh_from_db()
    assert thread.category == sibling_category

    user_thread.refresh_from_db()
    assert user_thread.category == sibling_category

    thread_relations.assert_category(sibling_category)
    user_thread_relations.assert_category(sibling_category)


def test_move_threads_moves_thread_to_new_category(
    thread_relations_factory, thread, sibling_category
):
    thread_relations = thread_relations_factory(thread)

    move_threads(thread, sibling_category)

    thread.refresh_from_db()
    assert thread.category == sibling_category

    thread_relations.assert_category(sibling_category)
