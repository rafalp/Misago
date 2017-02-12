from rest_framework import serializers

from django.test import TestCase

from misago.categories.models import Category
from misago.core.serializers import Subsettable
from misago.threads import testutils
from misago.threads.models import Thread


class SubsettableSerializerTests(TestCase):
    def test_create_subset_serializer(self):
        """classmethod subset creates new serializer"""
        category = Category.objects.get(slug='first-category')
        thread = testutils.post_thread(category=category)

        fields = ('id', 'title', 'replies', 'last_poster_name')

        serializer = TestSerializer.subset(*fields)
        self.assertEqual(
            serializer.__name__,
            'TestSerializerIdTitleRepliesLastPosterNameSubset'
        )
        self.assertEqual(serializer.Meta.fields, fields)

        serialized_thread = serializer(thread).data
        self.assertEqual(serialized_thread, {
            'id': thread.id,
            'title': thread.title,
            'replies': thread.replies,
            'last_poster_name': thread.last_poster_name,
        })

        self.assertFalse(TestSerializer.Meta.fields == fields)


class TestSerializer(serializers.ModelSerializer, Subsettable):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'replies',
            'has_unapproved_posts',
            'started_on',
            'last_post_on',
            'last_post_is_event',
            'last_post',
            'last_poster_name',
            'is_unapproved',
            'is_hidden',
            'is_closed',
            'weight',

            'url',
        )

    def get_url(self, obj):
        return {
            'index': obj.get_absolute_url(),
            'new_post': obj.get_new_post_url(),
            'last_post': obj.get_last_post_url(),
            'unapproved_post': obj.get_unapproved_post_url(),
            'last_poster': self.get_last_poster_url(obj),
        }
