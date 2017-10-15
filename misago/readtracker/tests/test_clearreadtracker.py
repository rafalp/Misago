from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from misago.categories.models import Category
from misago.conf import settings
from misago.readtracker.management.commands import clearreadtracker
from misago.readtracker.models import PostRead
from misago.threads import testutils


UserModel = get_user_model()


class ClearReadTrackerTests(TestCase):
    def setUp(self):
        self.user_a = UserModel.objects.create_user("UserA", "testa@user.com", 'Pass.123')
        self.user_b = UserModel.objects.create_user("UserB", "testb@user.com", 'Pass.123')

        self.category = Category.objects.get(slug='first-category')

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
            user=self.user_a,
            category=self.category,
            thread=thread,
            post=thread.first_post,
            last_read_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF / 4)
        )
        deleted = PostRead.objects.create(
            user=self.user_b,
            category=self.category,
            thread=thread,
            post=thread.first_post,
            last_read_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF * 2)
        )

        command = clearreadtracker.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, "Deleted 1 expired entries")

        PostRead.objects.get(pk=existing.pk)
        with self.assertRaises(PostRead.DoesNotExist):
            PostRead.objects.get(pk=deleted.pk)
