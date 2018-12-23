from django.core.management import BaseCommand

from ....conf import settings
from ...signals import remove_old_ips


class Command(BaseCommand):
    help = "Removes users IPs stored for longer than set in MISAGO_IP_STORE_TIME."

    def handle(self, *args, **options):
        if not settings.MISAGO_IP_STORE_TIME:
            self.stdout.write("Old IP removal is disabled.")
            return

        remove_old_ips.send(sender=self)

        self.stdout.write(
            "IP addresses older than %s days have been removed."
            % settings.MISAGO_IP_STORE_TIME
        )
