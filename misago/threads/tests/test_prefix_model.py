from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.forums.models import Forum

from misago.threads.models import Prefix


class PrefixesManagerTests(TestCase):
    def setUp(self):
        Prefix.objects.clear_cache()

    def test_get_cached_prefixes(self):
        """get_cached_prefixes and get_cached_prefixes_dict work as intented"""
        test_prefixes = (
            Prefix.objects.create(name="Prefix 1"),
            Prefix.objects.create(name="Prefix 2"),
            Prefix.objects.create(name="Prefix 3"),
            Prefix.objects.create(name="Prefix 4"),
        )

        db_prefixes = Prefix.objects.get_cached_prefixes()
        self.assertEqual(len(db_prefixes), len(test_prefixes))
        for prefix in db_prefixes:
            self.assertIn(prefix, test_prefixes)

        db_prefixes = Prefix.objects.get_cached_prefixes_dict()
        self.assertEqual(len(db_prefixes), len(test_prefixes))
        for prefix in test_prefixes:
            self.assertEqual(db_prefixes[prefix.pk], prefix)

    def test_get_forum_prefixes(self):
        """get_forum_prefixes returns prefixes for forum"""
        forum = Forum.objects.all_forums().filter(role='forum')[:1][0]

        test_prefixes = (
            Prefix.objects.create(name="Prefix 1"),
            Prefix.objects.create(name="Prefix 2"),
            Prefix.objects.create(name="Prefix 3"),
            Prefix.objects.create(name="Prefix 4"),
        )

        test_prefixes[0].forums.add(forum)
        test_prefixes[2].forums.add(forum)

        forum_prefixes = Prefix.objects.get_forum_prefixes(forum)
        self.assertEqual(len(forum_prefixes), 2)
        self.assertIn(test_prefixes[0], forum_prefixes)
        self.assertIn(test_prefixes[2], forum_prefixes)
        self.assertNotIn(test_prefixes[1], forum_prefixes)
        self.assertNotIn(test_prefixes[3], forum_prefixes)
