from django.contrib.contenttypes.models import ContentType

from ...categories.models import Category
from ..models import ThreadEvent


def test_thread_event_model_content_model_returns_model_type():
    ct = ContentType(app_label="misago_categories", model="category")
    thread_event = ThreadEvent(content_type=ct)
    assert thread_event.content_model == Category


def test_thread_event_model_get_object_id_returns_id_if_content_type_is_valid():
    ct = ContentType(app_label="misago_categories", model="category")
    thread_event = ThreadEvent(content_type=ct, object_id=1234)
    assert thread_event.get_object_id("misago_categories.category") == 1234


def test_thread_event_model_get_object_id_doesnt_return_id_if_content_type_is_invalid():
    ct = ContentType(app_label="misago_categories", model="category")
    thread_event = ThreadEvent(content_type=ct, object_id=1234)
    assert thread_event.get_object_id("misago_thread.post") is None


def test_thread_event_model_get_object_id_doesnt_return_id_if_content_type_is_not_set():
    thread_event = ThreadEvent()
    assert thread_event.get_object_id("misago_thread.post") is None


def test_thread_event_model_get_object_id_doesnt_return_id_if_object_id_is_not_set():
    ct = ContentType(app_label="misago_categories", model="category")
    thread_event = ThreadEvent(content_type=ct)
    assert thread_event.get_object_id("misago_categories.category") is None


def test_thread_event_model_clear_content_object_clears_model_attrs():
    ct = ContentType(app_label="misago_categories", model="category")
    thread_event = ThreadEvent(content_type=ct, object_id=1234)

    assert thread_event.content_type
    assert thread_event.object_id

    thread_event.clear_content_object()
    assert thread_event.content_type is None
    assert thread_event.object_id is None
    assert thread_event.content_object is None
