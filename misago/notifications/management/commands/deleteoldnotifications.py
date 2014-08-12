from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.notifications.models import Notification


class Command(BaseCommand):
    help = 'Deletes old notifications.'

    def handle(self, *args, **options):
        cutoff = timedelta(days=settings.MISAGO_NOTIFICATIONS_MAX_AGE)
        cutoff_date = timezone.now() - cutoff

        Notification.objects.filter(date__lte=cutoff_date).delete()
        self.stdout.write('Old notifications have been deleted.')
