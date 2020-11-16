from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from ...threads import test
from ..management.commands import synchronizecategories
from ..models import Category


class SynchronizeCategoriesTests(TestCase):
    def test_categories_sync(self):
        """command synchronizes categories"""
        category = Category.objects.all_categories()[:1][0]

        threads = [test.post_thread(category) for _ in range(10)]
        for thread in threads:
            [test.reply_thread(thread) for _ in range(5)]

        category.threads = 0
        category.posts = 0

        command = synchronizecategories.Command()

        out = StringIO()
        call_command(command, stdout=out)

        category = Category.objects.get(id=category.id)
        self.assertEqual(category.threads, 10)
        self.assertEqual(category.posts, 60)

        command_output = out.getvalue().splitlines()[-1].strip()
        self.assertTrue(command_output.startswith("Synchronized 3 categories in"))
