from django.contrib.contenttypes.models import ContentType
from pytest import mark

from ...categories.models import Category
from ...threads.models import Post
from ..models import ThreadEvent


def test_thread_event_model_content_model_returns_model_type():
    ct = ContentType.objects.get_for_model(Category)
    thread_event = ThreadEvent(content_type=ct)
    assert thread_event.content_type_model == Category


@mark.django_db
def test_thread_event_model_get_object_id_returns_id_if_content_type_is_valid():
    ct = ContentType.objects.get_for_model(Category)
    thread_event = ThreadEvent(content_type=ct, object_id=1234)
    assert thread_event.get_object_id_for_type(Category) == 1234


@mark.django_db
def test_thread_event_model_get_object_id_doesnt_return_id_if_content_type_is_invalid():
    ct = ContentType.objects.get_for_model(Category)
    thread_event = ThreadEvent(content_type=ct, object_id=1234)
    assert thread_event.get_object_id_for_type(Post) is None


def test_thread_event_model_get_object_id_doesnt_return_id_if_content_type_is_not_set():
    thread_event = ThreadEvent()
    assert thread_event.get_object_id_for_type(Post) is None


def test_thread_event_model_get_object_id_doesnt_return_id_if_object_id_is_not_set():
    ct = ContentType.objects.get_for_model(Category)
    thread_event = ThreadEvent(content_type=ct)
    assert thread_event.get_object_id_for_type(Category) is None


def test_thread_event_model_clear_content_object_clears_model_attrs():
    ct = ContentType.objects.get_for_model(Category)
    thread_event = ThreadEvent(content_type=ct, object_id=1234)

    assert thread_event.content_type
    assert thread_event.object_id

    thread_event.content_object = None
    assert thread_event.content_type is None
    assert thread_event.object_id is None
    assert thread_event.content_object is None
