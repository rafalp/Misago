from ...categories.models import Category
from ..create import create_test_thread_event
from ..models import ThreadEvent


def test_thread_event_queryset_content_object_filters_by_content_object(
    user, thread, default_category, sibling_category
):
    create_test_thread_event(thread)
    create_test_thread_event(thread, content_object=user)
    create_test_thread_event(thread, content_object=sibling_category)

    thread_event = create_test_thread_event(thread, content_object=default_category)

    assert ThreadEvent.objects.content_object(default_category).count() == 1
    assert ThreadEvent.objects.content_object(default_category).first() == thread_event


def test_thread_event_queryset_content_type_filters_by_content_type_using_model_instance(
    user, thread, default_category, sibling_category
):
    create_test_thread_event(thread)
    create_test_thread_event(thread, content_object=user)
    create_test_thread_event(thread, content_object=sibling_category)
    create_test_thread_event(thread, content_object=default_category)

    assert ThreadEvent.objects.content_type(default_category).count() == 2


def test_thread_event_queryset_content_type_filters_by_content_type_using_model_type(
    user, thread, default_category, sibling_category
):
    create_test_thread_event(thread)
    create_test_thread_event(thread, content_object=user)
    create_test_thread_event(thread, content_object=sibling_category)
    create_test_thread_event(thread, content_object=default_category)

    assert ThreadEvent.objects.content_type(Category).count() == 2


def test_thread_event_queryset_clear_content_objects_clears_content_type_and_object_id(
    thread, default_category, sibling_category
):
    thread_event = create_test_thread_event(
        thread,
        detail=default_category.name,
        content_object=default_category,
    )
    other_thread_event = create_test_thread_event(
        thread,
        detail=sibling_category.name,
        content_object=sibling_category,
    )

    ThreadEvent.objects.content_object(default_category).clear_content_objects()

    thread_event.refresh_from_db()
    assert thread_event.detail == default_category.name
    assert thread_event.content_type is None
    assert thread_event.object_id is None

    other_thread_event.refresh_from_db()
    assert other_thread_event.detail == sibling_category.name
    assert other_thread_event.content_type.app_label == "misago_categories"
    assert other_thread_event.content_type.name == "category"
    assert other_thread_event.object_id == sibling_category.id
