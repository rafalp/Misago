from django.test import TestCase

from misago.core.models import CacheVersion
from misago.core.pgutils import chunk_queryset


class ChunkQuerysetTest(TestCase):
    def setUp(self):
        # clear table
        CacheVersion.objects.all().delete()

        # create 100 items
        items_ids = []
        for _ in range(100):
            obj = CacheVersion.objects.create(cache='nomatter')
            items_ids.append(obj.id)
        self.items_ids = list(reversed(items_ids))

    def test_chunk_queryset(self):
        """chunk_queryset utility chunks queryset but returns all items"""
        chunked_ids = []

        with self.assertNumQueries(21):
            queryset = CacheVersion.objects.all()
            for obj in chunk_queryset(queryset, chunk_size=5):
                chunked_ids.append(obj.id)

        self.assertEqual(chunked_ids, self.items_ids)
            
    def test_chunk_shrinking_queryset(self):
        """chunk_queryset utility chunks queryset in delete action"""
        with self.assertNumQueries(121):
            queryset = CacheVersion.objects.all()
            for obj in chunk_queryset(queryset, chunk_size=5):
                obj.delete()

        self.assertEqual(CacheVersion.objects.count(), 0)
            