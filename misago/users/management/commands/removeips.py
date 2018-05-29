from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError

from misago.conf import settings
from misago.core.utils import ANONYMOUS_IP
from misago.users.signals import anonymize_old_ips

class Command(BaseCommand):
    help =  "Anonymizes users IPs stored for longer than set in MISAGO_IP_STORE_TIME."
    
    def handle(self, *args, **options):
      if not settings.MISAGO_IP_STORE_TIME:
        print("IP anonymization is disabled!")
        return
      else:
        anonymize_old_ips.send(sender=self)
        self.stdout.write("IP addresses older than {:d} days have been anonymized!".format(not settings.MISAGO_IP_STORE_TIME))

