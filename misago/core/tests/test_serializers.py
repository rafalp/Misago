from rest_framework import serializers

from ...threads.models import Thread
from ..serializers import MutableFields


class Serializer(serializers.ModelSerializer, MutableFields):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "replies",
            "has_unapproved_posts",
            "started_at",
            "last_posted_at",
            "last_post_is_event",
            "last_post",
            "last_poster_name",
            "is_unapproved",
            "is_hidden",
            "is_closed",
            "weight",
        ]


def test_mutable_fields_serialized_subset_fields(thread_factory, default_category):
    thread = thread_factory(default_category)

    fields = ["id", "title", "replies", "last_poster_name"]

    serializer = Serializer.subset_fields(*fields)
    assert serializer.__name__ == "SerializerIdTitleRepliesLastPosterNameSubset"
    assert serializer.Meta.fields == fields
    assert Serializer.Meta.fields != serializer.Meta.fields

    serialized_thread = serializer(thread).data
    assert serialized_thread == {
        "id": thread.id,
        "title": thread.title,
        "replies": thread.replies,
        "last_poster_name": thread.last_poster_name,
    }


def test_mutable_fields_serialized_exclude_fields(thread_factory, default_category):
    thread = thread_factory(default_category)

    kept_fields = ["id", "title", "weight"]
    removed_fields = list(set(Serializer.Meta.fields) - set(kept_fields))

    serializer = Serializer.exclude_fields(*removed_fields)
    assert serializer.__name__ == "SerializerIdTitleWeightSubset"
    assert serializer.Meta.fields == kept_fields
    assert Serializer.Meta.fields != serializer.Meta.fields

    serialized_thread = serializer(thread).data
    assert serialized_thread == {
        "id": thread.id,
        "title": thread.title,
        "weight": thread.weight,
    }


def test_mutable_fields_serialized_extend_fields(thread_factory, default_category):
    thread = thread_factory(default_category)

    serializer = Serializer.extend_fields("category")

    serialized_thread = serializer(thread).data
    assert serialized_thread["category"] == default_category.id
