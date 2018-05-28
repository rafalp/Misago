from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from misago.core.utils import ANONYMOUS_IP
from misago.users.signals import anonymize_old_ips

MISAGO_IP_STORE_TIME = 33300
class Command(BaseCommand):
    help =  "Anonymizes users IPs stored for longer than set in MISAGO_IP_STORE_TIME."

    def handle(self, *args, **options):
      anonymize_old_ips.send(sender=self)
      self.stdout.write("IP addresses older than " + str(MISAGO_IP_STORE_TIME) + " days have been anonymized!")
