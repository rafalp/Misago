from ...categories.models import Category
from ..create import create_test_thread_update
from ..models import ThreadUpdate


def test_thread_update_queryset_context_object_filters_by_context_object(
    user, thread, default_category, sibling_category
):
    create_test_thread_update(thread)
    create_test_thread_update(thread, context_object=user)
    create_test_thread_update(thread, context_object=sibling_category)

    thread_update = create_test_thread_update(thread, context_object=default_category)

    assert ThreadUpdate.objects.context_object(default_category).count() == 1
    assert (
        ThreadUpdate.objects.context_object(default_category).first() == thread_update
    )


def test_thread_update_queryset_context_type_filters_by_context_type_using_model_instance(
    user, thread, default_category, sibling_category
):
    create_test_thread_update(thread)
    create_test_thread_update(thread, context_object=user)
    create_test_thread_update(thread, context_object=sibling_category)
    create_test_thread_update(thread, context_object=default_category)

    assert ThreadUpdate.objects.context_type(default_category).count() == 2


def test_thread_update_queryset_context_type_filters_by_context_type_using_model_type(
    user, thread, default_category, sibling_category
):
    create_test_thread_update(thread)
    create_test_thread_update(thread, context_object=user)
    create_test_thread_update(thread, context_object=sibling_category)
    create_test_thread_update(thread, context_object=default_category)

    assert ThreadUpdate.objects.context_type(Category).count() == 2


def test_thread_update_queryset_clear_context_objects_clears_context_type_and_context_id(
    thread, default_category, sibling_category
):
    thread_update = create_test_thread_update(
        thread,
        context=default_category.name,
        context_object=default_category,
    )
    other_thread_update = create_test_thread_update(
        thread,
        context=sibling_category.name,
        context_object=sibling_category,
    )

    ThreadUpdate.objects.context_object(default_category).clear_context_objects()

    thread_update.refresh_from_db()
    assert thread_update.context == default_category.name
    assert thread_update.context_type is None
    assert thread_update.context_id is None

    other_thread_update.refresh_from_db()
    assert other_thread_update.context == sibling_category.name
    assert other_thread_update.context_type == "misago_categories.category"
    assert other_thread_update.context_id == sibling_category.id
