from ...categories.models import Category
from ..models import ThreadEvent


def test_thread_event_model_context_model_returns_model_type():
    thread_event = ThreadEvent(context_type="misago_categories.category")
    assert thread_event.context_model == Category


def test_thread_event_model_context_model_returns_none_for_invalid_context_app():
    thread_event = ThreadEvent(context_type="misago_invalid.category")
    assert thread_event.context_model is None


def test_thread_event_model_context_model_returns_none_for_invalid_context_model():
    thread_event = ThreadEvent(context_type="misago_categories.invalid")
    assert thread_event.context_model is None


def test_thread_event_model_get_context_id_returns_id_if_context_type_is_valid():
    thread_event = ThreadEvent(
        context_type="misago_categories.category", context_id=1234
    )
    assert thread_event.get_context_id("misago_categories.category") == 1234


def test_thread_event_model_get_context_id_doesnt_return_id_if_context_type_is_invalid():
    thread_event = ThreadEvent(
        context_type="misago_categories.category", context_id=1234
    )
    assert thread_event.get_context_id("misago_thread.post") is None


def test_thread_event_model_get_context_id_doesnt_return_id_if_context_type_is_not_set():
    thread_event = ThreadEvent()
    assert thread_event.get_context_id("misago_thread.post") is None


def test_thread_event_model_get_context_id_doesnt_return_id_if_context_id_is_not_set():
    thread_event = ThreadEvent(context_type="misago_categories.category")
    assert thread_event.get_context_id("misago_categories.category") is None


def test_thread_event_model_clear_context_object_clears_model_attrs():
    thread_event = ThreadEvent(
        context_type="misago_categories.category", context_id=1234
    )

    assert thread_event.context_type
    assert thread_event.context_id

    thread_event.clear_context_object()
    assert thread_event.context_type is None
    assert thread_event.context_id is None
