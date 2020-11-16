from django.core.management.base import BaseCommand
from django.utils import timezone

from ....cache.versions import get_cache_versions
from ....users import BANS_CACHE
from ...models import Ban, BanCache


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
        self.stdout.write("Bans invalidated: %s" % expired_count)

    def handle_bans_caches(self):
        queryset = BanCache.objects.filter(expires_on__lt=timezone.now())

        expired_count = queryset.count()
        queryset.delete()

        cache_versions = get_cache_versions()
        queryset = BanCache.objects.exclude(cache_version=cache_versions[BANS_CACHE])

        expired_count += queryset.count()
        queryset.delete()

        self.stdout.write("Ban caches emptied: %s" % expired_count)
