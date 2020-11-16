from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from .. import test
from ...categories.models import Category
from ..management.commands import updatepostschecksums
from ..models import Post


class UpdatePostsChecksumsTests(TestCase):
    def test_no_posts_to_update(self):
        """command works when there are no posts"""
        command = updatepostschecksums.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, "No posts were found")

    def test_posts_update(self):
        """command updates posts checksums"""
        category = Category.objects.all_categories()[:1][0]

        threads = [test.post_thread(category) for _ in range(5)]
        for _, thread in enumerate(threads):
            [test.reply_thread(thread) for _ in range(3)]
            thread.save()

        Post.objects.update(parsed="Hello world!")
        for post in Post.objects.all():
            self.assertFalse(post.is_valid)

        command = updatepostschecksums.Command()

        out = StringIO()
        call_command(command, stdout=out)

        command_output = out.getvalue().splitlines()[-1].strip()
        self.assertEqual(command_output, "Updated 20 posts checksums")

        for post in Post.objects.all():
            self.assertTrue(post.is_valid)
