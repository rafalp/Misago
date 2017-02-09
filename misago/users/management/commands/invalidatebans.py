from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.core import cachebuster
from misago.users.models import Ban, BanCache


class Command(BaseCommand):
    help = (
        "Runs maintenance on Misago bans system, "
        "invalidating expired bans and pruning caches."
    )

    def handle(self, *args, **options):
        self.handle_expired_bans()
        self.handle_bans_caches()

    def handle_expired_bans(self):
        queryset = Ban.objects.filter(is_checked=True)
        queryset = queryset.filter(expires_on__lt=timezone.now())

        expired_count = queryset.update(is_checked=False)
        self.stdout.write('Bans invalidated: %s' % expired_count)

    def handle_bans_caches(self):
        queryset = BanCache.objects.filter(expires_on__lt=timezone.now())

        expired_count = queryset.count()
        queryset.delete()

        bans_version = cachebuster.get_version('misago_bans')
        queryset = BanCache.objects.filter(bans_version__lt=bans_version)

        expired_count += queryset.count()
        queryset.delete()

        self.stdout.write('Ban caches emptied: %s' % expired_count)
