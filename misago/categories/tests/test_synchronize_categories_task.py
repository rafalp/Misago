from ..tasks import synchronize_categories


def test_synchronize_categories_task_synchronizes_threads(
    thread_factory, default_category, sibling_category
):
    thread_factory(default_category)
    thread_factory(default_category)
    thread_factory(default_category)
    thread_factory(sibling_category)
    thread_factory(sibling_category)

    synchronize_categories([default_category.id, sibling_category.id])

    default_category.refresh_from_db()
    assert default_category.threads == 3

    sibling_category.refresh_from_db()
    assert sibling_category.threads == 2
