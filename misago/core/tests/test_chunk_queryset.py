from django.test import TestCase

from ...cache.models import CacheVersion
from ..pgutils import chunk_queryset


class ChunkQuerysetTest(TestCase):
    def setUp(self):
        # clear table
        CacheVersion.objects.all().delete()

        items_pks = []
        for i in range(50):
            obj = CacheVersion.objects.create(cache="test%s" % i)
            items_pks.append(obj.pk)
        self.items_pks = list(sorted(items_pks, reverse=True))

    def test_chunk_queryset(self):
        """chunk_queryset utility chunks queryset but returns all items"""
        chunked_pks = []

        with self.assertNumQueries(11):
            queryset = CacheVersion.objects.order_by("cache")
            for obj in chunk_queryset(queryset, chunk_size=5):
                chunked_pks.append(obj.pk)

        self.assertEqual(chunked_pks, self.items_pks)

    def test_chunk_shrinking_queryset(self):
        """chunk_queryset utility chunks queryset in delete action"""
        with self.assertNumQueries(61):
            queryset = CacheVersion.objects.all()
            for obj in chunk_queryset(queryset, chunk_size=5):
                obj.delete()

        self.assertEqual(CacheVersion.objects.count(), 0)
