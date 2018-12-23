from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from ...categories.models import Category
from ...conf import settings
from ...threads import test
from ...users.test import create_test_user
from ..management.commands import clearreadtracker
from ..models import PostRead


class ClearReadTrackerTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")
        self.other_user = create_test_user("OtherUser", "otheruser@example.com")

        self.category = Category.objects.get(slug="first-category")

    def test_no_deleted(self):
        """command works when there are no attachments"""
        command = clearreadtracker.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, "No expired entries were found")

    def test_delete_expired_entries(self):
        """test deletes one expired tracker entry, but spares the other"""
        thread = test.post_thread(self.category)

        existing = PostRead.objects.create(
            user=self.user,
            category=self.category,
            thread=thread,
            post=thread.first_post,
            last_read_on=timezone.now()
            - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF / 4),
        )
        deleted = PostRead.objects.create(
            user=self.other_user,
            category=self.category,
            thread=thread,
            post=thread.first_post,
            last_read_on=timezone.now()
            - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF * 2),
        )

        command = clearreadtracker.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, "Deleted 1 expired entries")

        PostRead.objects.get(pk=existing.pk)
        with self.assertRaises(PostRead.DoesNotExist):
            PostRead.objects.get(pk=deleted.pk)
