from django.core.management import BaseCommand

from ....conf.shortcuts import get_dynamic_settings
from ...signals import remove_old_ips


class Command(BaseCommand):
    help = "Removes users IPs stored for longer than configured by administrator."

    def handle(self, *args, **options):
        settings = get_dynamic_settings()
        if not settings.ip_storage_time:
            self.stdout.write("Old IP removal is disabled.")
            return

        remove_old_ips.send(sender=self, ip_storage_time=settings.ip_storage_time)

        self.stdout.write(
            "IP addresses older than %s days have been removed."
            % settings.ip_storage_time
        )
