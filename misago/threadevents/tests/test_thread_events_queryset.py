from ...categories.models import Category
from ..create import create_test_thread_event
from ..models import ThreadEvent


def test_thread_event_queryset_context_object_filters_by_context_object(
    user, thread, default_category, sibling_category
):
    create_test_thread_event(thread)
    create_test_thread_event(thread, context_object=user)
    create_test_thread_event(thread, context_object=sibling_category)

    thread_event = create_test_thread_event(thread, context_object=default_category)

    assert ThreadEvent.objects.context_object(default_category).count() == 1
    assert ThreadEvent.objects.context_object(default_category).first() == thread_event


def test_thread_event_queryset_context_type_filters_by_context_type_using_model_instance(
    user, thread, default_category, sibling_category
):
    create_test_thread_event(thread)
    create_test_thread_event(thread, context_object=user)
    create_test_thread_event(thread, context_object=sibling_category)
    create_test_thread_event(thread, context_object=default_category)

    assert ThreadEvent.objects.context_type(default_category).count() == 2


def test_thread_event_queryset_context_type_filters_by_context_type_using_model_type(
    user, thread, default_category, sibling_category
):
    create_test_thread_event(thread)
    create_test_thread_event(thread, context_object=user)
    create_test_thread_event(thread, context_object=sibling_category)
    create_test_thread_event(thread, context_object=default_category)

    assert ThreadEvent.objects.context_type(Category).count() == 2


def test_thread_event_queryset_clear_context_objects_clears_context_type_and_context_id(
    thread, default_category, sibling_category
):
    thread_event = create_test_thread_event(
        thread,
        context=default_category.name,
        context_object=default_category,
    )
    other_thread_event = create_test_thread_event(
        thread,
        context=sibling_category.name,
        context_object=sibling_category,
    )

    ThreadEvent.objects.context_object(default_category).clear_context_objects()

    thread_event.refresh_from_db()
    assert thread_event.context == default_category.name
    assert thread_event.context_type is None
    assert thread_event.context_id is None

    other_thread_event.refresh_from_db()
    assert other_thread_event.context == sibling_category.name
    assert other_thread_event.context_type == "misago_categories.category"
    assert other_thread_event.context_id == sibling_category.id
