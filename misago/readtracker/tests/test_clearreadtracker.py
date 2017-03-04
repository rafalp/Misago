from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from misago.categories.models import Category
from misago.conf import settings
from misago.readtracker.management.commands import clearreadtracker
from misago.readtracker.models import CategoryRead, ThreadRead
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

    def test_delete_expired_category_entries(self):
        """test deletes one expired category tracker, but spares the other"""
        existing = CategoryRead.objects.create(
            user=self.user_a,
            category=self.category,
            last_read_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF / 4)
        )

        deleted = CategoryRead.objects.create(
            user=self.user_b,
            category=self.category,
            last_read_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF * 2)
        )

        command = clearreadtracker.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, "Deleted 1 expired entries")

        CategoryRead.objects.get(pk=existing.pk)
        with self.assertRaises(CategoryRead.DoesNotExist):
            CategoryRead.objects.get(pk=deleted.pk)

    def test_delete_expired_thread(self):
        """test deletes one expired thread tracker, but spares the other"""
        thread = testutils.post_thread(self.category)

        existing = ThreadRead.objects.create(
            user=self.user_a,
            category=self.category,
            thread=thread,
            last_read_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF / 4)
        )

        deleted = ThreadRead.objects.create(
            user=self.user_b,
            category=self.category,
            thread=thread,
            last_read_on=timezone.now() - timedelta(days=settings.MISAGO_READTRACKER_CUTOFF * 2)
        )

        command = clearreadtracker.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().strip()

        self.assertEqual(command_output, "Deleted 1 expired entries")

        ThreadRead.objects.get(pk=existing.pk)
        with self.assertRaises(ThreadRead.DoesNotExist):
            ThreadRead.objects.get(pk=deleted.pk)
