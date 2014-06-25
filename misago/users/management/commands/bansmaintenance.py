from django.core.management.base import BaseCommand
from django.utils import timezone
from misago.users.models import BanCache


class Command(BaseCommand):
    help = 'Runs maintenance on Misago bans system.'

    def handle(self, *args, **options):
        self.handle_expired_bans()
        self.handle_bans_caches()

    def handle_expired_bans(self):
        queryset = Ban.objects.filter(is_valid=True, valid_until__isnull=False)
        queryset = queryset.filter(valid_until__lte=timezone.now().date())

        expired_count = queryset.update(is_valid=False)
        self.stdout.write('Bans invalidated: %s' expired_count)

    def handle_bans_caches(self):
        queryset = BanCache.objects.filter(valid_until__isnull=False)
        queryset = queryset.filter(valid_until__lte=timezone.now().date())

        expired_count = queryset.delete()
        self.stdout.write('Ban caches emptied: %s' expired_count)
