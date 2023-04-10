from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ....conf.shortcuts import get_dynamic_settings
from ...models import Notification


class Command(BaseCommand):
    help = "Deletes old notifications"

    def handle(self, *args, **options):
        settings = get_dynamic_settings()
        cutoff_date = timezone.now() - timedelta(
            days=settings.delete_notifications_older_than
        )
        queryset = Notification.objects.filter(created_at__lt=cutoff_date)
        deleted_count = queryset.count()

        if deleted_count:
            queryset.delete()
            message = "\n\nDeleted %s old notifications." % deleted_count
        else:
            message = "\n\nNo old notifications have been deleted."

        self.stdout.write(message)
