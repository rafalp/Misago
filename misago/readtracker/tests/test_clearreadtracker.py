from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from misago.categories.models import Category
from misago.conf import settings
from misago.readtracker.management.commands import clearreadtracker
from misago.readtracker.models import PostRead
from misago.threads import testutils
from misago.users.testutils import create_test_user


class ClearReadTrackerTests(TestCase):
    def setUp(self):
        self.user_1 = create_test_user("User1", "user1@example.com")
        self.user_2 = create_test_user("User2", "user2@example.com")

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
        thread = testutils.post_thread(self.category)

        existing = PostRead.objects.create(
            user=self.user_1,
            category=self.category,
            thread=thread,
            post=thread.first_post,
            last_read_on=timezone.now()
            - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF / 4),
        )
        deleted = PostRead.objects.create(
            user=self.user_2,
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
